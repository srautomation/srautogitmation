from sr_automation.utils.Collector import Collector, CollectorHandler
from functools import partial
from bunch import Bunch
import time

from logbook import Logger
log = Logger("Resources")

class Resources(object):
    COMMAND = '"busybox head -1 /proc/stat;busybox head -4 /proc/meminfo; cat /sys/class/power_supply/*bat*/capacity; cat /proc/*/stat 2>/dev/null"'
    SAMPLES_DELTA = 15
    def __init__(self, android):
        self._android = android
        self._resources_handler = CollectorHandler()
        self._samples = []
        self._own_pids = set()

    def set_own_pids(self, pids = []):
        self._own_pids = set(pids)
    
    def _parse(self, lines):
        cpu = Bunch(zip(["user", "nice", "system", "idle", "iowait", "irq", "softirq", "steal", "guest", "guest_nice"], map(int, lines[0].split(' ')[2:])))
        cpu.total  = cpu.user + cpu.nice + cpu.system + cpu.idle + cpu.iowait + cpu.irq + cpu.softirq + cpu.steal + cpu.guest + cpu.guest_nice
        cpu.active = cpu.total - (cpu.idle + cpu.iowait)
        mem = Bunch(zip(["total", "free", "buffers", "cache"], [int(line.split(' ')[-2]) for line in lines[1:5]]))
        mem.used = mem.total - mem.free - mem.buffers - mem.cache
        bat = Bunch(percent = int(lines[5]) / 100.0)
        processes = {}
        for line in lines[6:]:
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
            process.cpu.percent = 1.0 * (_temp.cpu.user + _temp.cpu.system) / current.delta.cpu.active
            delta_processes[pid] = _temp
        current.delta.processes = delta_processes
        return current

    def _factor_out_own_processes(self, sample):
        sample.cpu.own = sum([process.cpu.percent for (pid, process) in sample.processes.items() if pid in self._own_pids])
        sample.cpu.percent -= sample.cpu.own
        return sample

    def _input(self, pattern = None):
        sample = self._parse(self._android.cmd('shell ' + Resources.COMMAND).stdout.readlines())
        sample.time = time.time()
        self._samples.append(sample)
        if len(self._samples) < Resources.SAMPLES_DELTA:
            return None
        sample_oldest = self._samples.pop(0)
        sample = self._factor_out_own_processes(self._diff(sample, sample_oldest))
        #log.warn("CPU Percent = %f, own = %f" % (sample.cpu.percent, sample.cpu.own))
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
                    if collected:
                        if name == "max":
                            return max(collected)
                        elif name == "min":
                            return min(collected)
                        elif name == "avg":
                            return 1.0 * sum(collected) / len(collected)
                    else: return 0

                else:
                    return getattr(_self, name)
        return _Measured()

if __name__ == "__main__":
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    resources = Resources(android)
    with resources.measure():
        time.sleep(5)
    print resources.measured.mem.avg
    print resources.measured.bat.min
    print resources.measured.cpu.max

