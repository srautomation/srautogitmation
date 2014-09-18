from infrastructure.utils.Collector import Collector, CollectorHandler
from bunch import Bunch
from functools import partial
import re
import time

from logbook import Logger
log = Logger("Resources")

class Resources(object):
    SAMPLES_TO_COLLECT = 10
    TOP_REGEXPS = Bunch(
        tasks = re.compile("Tasks:.+?(?P<total>\d+).+?(?P<running>\d+).+?(?P<sleeping>\d+).+?(?P<stopped>\d+).+?(?P<zombie>\d+)"),
        cpu   = re.compile("%Cpu.+?(?P<user>[\d\.]+).+?(?P<system>[\d\.]+).+?(?P<nice>[\d\.]+).+?(?P<idle>[\d\.]+).+?(?P<waiting>[\d\.]+).+?(?P<hardware_irq>[\d\.]+).+?(?P<software_interrupts>[\d\.]+).+?(?P<stolen>[\d\.]+).+?"),
        mem   = re.compile("KiB Mem.+?(?P<total>\d+).+?(?P<used>\d+).+?(?P<free>\d+).+?(?P<buffers>\d+)"),
        swap   = re.compile("KiB Swap.+?(?P<total>\d+).+?(?P<used>\d+).+?(?P<free>\d+).+?(?P<cached>\d+)"),
        process = re.compile("\s*(?P<pid>[^\s]+)\s+(?P<user>[^\s]+)\s+(?P<priority>[^\s]+)\s+(?P<nice>[^\s]+)\s+(?P<virt>[^\s]+)\s+(?P<res>[^\s]+)\s+(?P<shr>[^\s]+)\s+(?P<s>[^\s]+)\s+(?P<pcpu>[^\s]+)\s+(?P<pmem>[^\s]+)\s+(?P<time>[^\s]+)\s+(?P<command>.+)"),
        )
    
    def __init__(self, rpyc, cmd, own_processes):
        self._rpyc = rpyc
        self._shell_cmd = cmd
        self._resources_handler = CollectorHandler()
        self._samples = []
        self._own_processes = own_processes

    def _is_own_process(self, command_line):
        return sum([(own_process in command_line) for own_process in self._own_processes]) > 0

    def _ps(self):
        lines = self._shell_cmd("ps --no-headers -eo pid,pcpu,pmem,cmd").stdout.readlines()

        # parse lines
        lines = [re.split("\s+", line.strip(), 3) for line in lines]
        processes = [Bunch(pid = int(pid), pcpu = float(pcpu), pmem = float(pmem), command = comm) for (pid, pcpu, pmem, comm) in lines]

        # return and sum pcpu/pmem
        return Bunch(
                processes = processes, 
                total_pcpu = sum([process.pcpu for process in processes]),
                total_pmem = sum([process.pmem for process in processes])
                )

    def _top(self):
        lines = self._shell_cmd("top -b -d 1 -n1").stdout.readlines()
        tasks = Bunch({name: int(value)   for name, value in Resources.TOP_REGEXPS.tasks.match(lines[1]).groupdict().items()})
        cpu   = Bunch({name: float(value) for name, value in Resources.TOP_REGEXPS.cpu.match(lines[2]).groupdict().items()})
        mem   = Bunch({name: float(value) for name, value in Resources.TOP_REGEXPS.mem.match(lines[3]).groupdict().items()})
        swap  = Bunch({name: float(value) for name, value in Resources.TOP_REGEXPS.swap.match(lines[4]).groupdict().items()})
        textual_processes = [Bunch(Resources.TOP_REGEXPS.process.match(line).groupdict()) for line in lines[7:]]

        #--------------------------------------
        # remove own process from calcluation
        ps = self._ps()
        own_processes_pids = [process.pid for process in ps.processes if self._is_own_process(process.command)]
        own_processes_cpu = sum([float(process.pcpu) for process in textual_processes if int(process.pid.strip()) in own_processes_pids])
        log.info("Own processes cpu percent = %f" % own_processes_cpu)
        
        # calculate actual cpu usage (total - idle - own_processes)
        cpu.actual = 1.0 * ((cpu.user + cpu.system + cpu.nice + cpu.waiting + cpu.hardware_irq + cpu.software_interrupts + cpu.stolen) - own_processes_cpu) / 100.0
        return Bunch(tasks = tasks, cpu = cpu, mem = mem, swap = swap)



    def _cpu_percent_from_samples():
        if (len(self._samples) >= Resources.SAMPLES_TO_COLLECT):
            oldest = self._samples.pop(0)
            # calculate CPU percent:
            idle      = sample.cpu.idle + sample.cpu.iowait
            prev_idle = oldest.cpu.idle + oldest.cpu.iowait
            sample.cpu.percent = (1.0 * (sample.cpu.total - oldest.cpu.total) - (idle - prev_idle)) / (sample.cpu.total - oldest.cpu.total)
            if sample.cpu.percent < 0:
                sample.cpu.percent = 0

    def _input(self, pattern = None):
        sample = Bunch(
                mem = Bunch(free = 0, used = 0, cache = 0),
                cpu = Bunch(idle = 0, iowait = 0, kernel = 0, user = 0, total = 0, percent = 0),
                bat = Bunch(percent = 0)
                )

        statgrab_text = self._shell_cmd("statgrab -u mem.free mem.used mem.cache cpu.idle cpu.iowait cpu.total").stdout.read()
        sample.mem.free, sample.mem.used, sample.mem.cache, sample.cpu.idle, sample.cpu.iowait, sample.cpu.total = map(float, statgrab_text.split("\n")[:-1])
        sample.mem.used += sample.mem.cache
        sample.mem.free -= sample.mem.cache

        battery_path = [x for x in self._rpyc.modules.os.listdir("/sys/class/power_supply") if 'bat' in x][0]
        sample.bat.percent = int(self._rpyc.builtin.file("/sys/class/power_supply/%s/capacity" % battery_path, "r").read())

        if (len(self._samples) >= Resources.SAMPLES_TO_COLLECT):
            oldest = self._samples.pop(0)
            # calculate CPU percent:
            idle      = sample.cpu.idle + sample.cpu.iowait
            prev_idle = oldest.cpu.idle + oldest.cpu.iowait
            sample.cpu.percent = (1.0 * (sample.cpu.total - oldest.cpu.total) - (idle - prev_idle)) / (sample.cpu.total - oldest.cpu.total)
            if sample.cpu.percent < 0:
                sample.cpu.percent = 0

        top = self._top()
        sample.cpu.percent = top.cpu.actual
        log.info("CPU Percent = %f" % sample.cpu.percent)
        self._samples.append(sample)
        return sample

    def measure(self, pattern = None):
        input_method = partial(self._input, pattern)
        class wrapper(object):
            def __enter__(_self):
                current_time = time.time()
                log.info("measure started at: %s" % (time.ctime(current_time)))
                _self.collector = Collector(input_method)
                _self.collector.add(self._resources_handler)
                _self.collector.start()
                
            def __exit__(_self, type, value, tb):
                _self.collector.stop()
                current_time = time.time()
                log.info("measure stopped at: %s" % (time.ctime(current_time)))
        return wrapper()

    @property
    def measured(self):
        class _Measured(object):
            def __init__(_self, action = None):
               _self.action = action

            def __getitem__(_self, index):
                return self._resources_handler.collected[index]
           
            def __getattr__(_self, name):
                if (_self.action is None) and (name in ["cpu", "mem", "bat"]):
                    return _Measured(action = name)

                elif (_self.action is not None) and (name in ["all", "min", "max", "avg"]):
                    if _self.action == "cpu":
                        collected = [x.cpu.percent for (t, x) in self._resources_handler.collected]
                    elif _self.action == "mem":
                        collected = [x.mem.used for (t, x) in self._resources_handler.collected]
                    elif _self.action == "bat":
                        collected = [x.bat.percent for (t, x) in self._resources_handler.collected]

                    if name == "all":
                        return collected
                    elif name == "max":
                        return max(collected)
                    elif name == "min":
                        return min(collected)
                    elif name == "avg":
                        return 1.0 * sum(collected) / len(collected)
                else:
                    return getattr(_self, name)
        return _Measured()
