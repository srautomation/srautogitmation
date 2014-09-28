from infrastructure.utils.Collector import Collector, CollectorHandler
from bunch import Bunch
from functools import partial
import re
import time

from logbook import Logger
log = Logger("Resources")

class Resources(object):
    COMMAND = 'head -1 /proc/stat; head -2 /proc/meminfo; cat /sys/class/power_supply/*bat*/capacity; cat /proc/*/stat 2>/dev/null'
    SAMPLES_DELTA = 15
    def __init__(self, rpyc, shell):
        self._rpyc = rpyc
        self._shell = shell
        self._resources_handler = CollectorHandler()
        self._samples = []

    def _parse(self, lines):
        cpu = Bunch(zip(["user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal", "guest", "guest_nice"], map(int, lines[0].split(' ')[2:])))
        cpu.total  = cpu.user + cpu.nice + cpu.system + cpu.idle + cpu.iowait + cpu.irq + cpu.softirq + cpu.steal + cpu.guest + cpu.guest_nice
        cpu.active = cpu.total - (cpu.idle + cpu.iowait)
        mem = Bunch(zip(["total", "free"], [int(line.split(' ')[-2]) for line in lines[1:3]]))
        mem.used = mem.total - mem.free
        bat = Bunch(percent = 0)#int(lines[3]))
        processes = {}
        for line in lines[4:]:
            cols = line.split(' ')
            pid, user, system = map(int, [cols[0], cols[13], cols[14]])
            processes[pid] = Bunch(cpu = Bunch(user = user, system = system))
        return Bunch(cpu = cpu, mem = mem, bat = bat, processes = processes)

    def _diff(self, current, old):
        current.delta = Bunch(cpu = Bunch(total = current.cpu.total - old.cpu.total, active = current.cpu.active - old.cpu.active))
        current.cpu.percent = 1.0 * current.delta.cpu.active / current.delta.cpu.total
        delta_processes = {}
        for pid, process in current.processes.items():
            if pid not in old.processes.keys():
                continue
            old_process = old.processes[pid]
            _temp = Bunch(cpu = Bunch(user = process.cpu.user - old_process.cpu.user, system = process.cpu.system - old_process.cpu.system))
            process.cpu.percent = (_temp.cpu.user + _temp.cpu.system) / current.cpu.active
            delta_processes[pid] = _temp
        current.delta.processes = delta_processes
        return current

    def _input(self, pattern = None):
        sample = self._parse(self._shell.shell(Resources.COMMAND).stdout.readlines())
        sample.time = time.time()
        self._samples.append(sample)
        if len(self._samples) < Resources.SAMPLES_DELTA:
            return None
        sample_oldest = self._samples.pop(0)
        sample = self._diff(sample, sample_oldest)

        # factor out own infrastructure CPU
#        own_pids = self._shell.own_processes.keys()
#        log.warn("PIDS = %r" % own_pids)
#        own_cpu  = sum([process.cpu.percent for (pid, process) in sample.processes.items() if pid in own_pids])
#        sample.cpu.own = own_cpu
#        sample.cpu.percent = sample.cpu.percent - sample.cpu.own_cpu

        log.warn("CPU Percent = %f" % sample.cpu.percent)
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
