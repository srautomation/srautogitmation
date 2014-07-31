from infrastructure.utils.Collector import Collector, CollectorHandler
from collections import namedtuple
from functools import partial
import time

from logbook import Logger
log = Logger("Vitals")

ATTRIBUTES = ["cpu", "battery", "mem", "disk"]
class Vitals(object):
    VitalCollection = namedtuple("VitalCollection", ATTRIBUTES)

    def __init__(self, cmd):
        self._shell_cmd = cmd
        self._vitals_handler = CollectorHandler()

    def _input(self, pattern = None):
        lines = self._shell_cmd("statgrab").stdout.readlines()
        return Vitals.VitalCollection(cpu = 0.5, battery = 0.5, mem = 1350, disk = 400)

    def measure(self, pattern = None):
        input_method = partial(self._input, pattern)
        class wrapper(object):
            def __enter__(_self):
                current_time = time.time()
                log.info("measure started at: %s" % (time.ctime(current_time)))
                _self.collector = Collector(input_method)
                _self.collector.add(self._vitals_handler)
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
                return self._vitals_handler.collected

            def __getitem__(_self, index):
                return self._vitals_handler.collected[index]
           
            def __getattr__(_self, name):
                if (_self.action is None) and (name in ATTRIBUTES):
                    return _Measured(action = name)
                elif (_self.action is not None) and (name in ["all", "min", "max", "avg"]):
                    collected = [getattr(x, _self.action) for (t, x) in self._vitals_handler.collected]
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
