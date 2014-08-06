from infrastructure.utils.Collector import Collector, CollectorHandler
from bunch import Bunch
from functools import partial
import time

from logbook import Logger
log = Logger("Resources")

class Resources(object):

    def __init__(self, cmd):
        self._shell_cmd = cmd
        self._resources_handler = CollectorHandler()
        self._previous = None

    def _input(self, pattern = None):
        sample = Bunch(
                mem = Bunch(free = 0, used = 0, total = 0),
                cpu = Bunch(idle = 0, iowait = 0, kernel = 0, user = 0, total = 0, percent = 0),
                bat = Bunch(percent = 0)
                )
        command_line = "statgrab -u mem.free mem.used cpu.idle cpu.iowait cpu.total;" +\
                "cat /sys/class/power_supply/*bat*/capacity;"
        lines = self._shell_cmd(command_line).stdout.read().split("\n")[:-1]
        values = [int(line) for line in lines]

        sample.mem.free, sample.mem.used, sample.cpu.idle, sample.cpu.iowait, sample.cpu.total, sample.bat.percent = values

        if self._previous is not None:
            # calculate CPU percent:
            idle      = sample.cpu.idle + sample.cpu.iowait
            prev_idle = self._previous.cpu.idle + self._previous.cpu.iowait
            sample.cpu.percent = (1.0 * (sample.cpu.total - self._previous.cpu.total) - (idle - prev_idle)) / (sample.cpu.total - self._previous.cpu.total)

        self._previous = sample
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

            @property
            def all(_self):
                return self._resources_handler.collected

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
