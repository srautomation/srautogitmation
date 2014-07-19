from utils import TimeIt
from Device import Device
from gevent import Timeout

class Tester(object):
    def __init__(self):
        self._timeit = TimeIt.TimeIt()

    @property
    def timeit(self):
        return self._timeit
    
    def device(self, device_id):
        return Device(device_id)

    def timeout(self, timeout):
        return Timeout(timeout)

