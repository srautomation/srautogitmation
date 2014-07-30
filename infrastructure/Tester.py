from utils import TimeIt
from Device import Device
from gevent import Timeout, with_timeout
import time

from logbook import Logger
log = Logger("Tester")

class Tester(object):
    def __init__(self):
        self._timeit = TimeIt.TimeIt()

    @property
    def timeit(self):
        return self._timeit
    
    def device(self, device_id, linux_ip = None):
        return Device(device_id, linux_ip)

    def timeout(self, timeout):
        log.info("Timeout started at: %s for %f seconds" % (time.ctime(), timeout))
        return Timeout(timeout, False)

if __name__ == "__main__":
    device_serial = "MedfieldB60440E1"
    tester = Tester()
    with tester.device(device_serial) as device:
        with tester.timeit.measure():
            with tester.timeout(15):
                print device.linux.cmd("uname -a").stdout.read()
                #time.sleep(40)
                #print device.linux.ldtp.launchapp("leafpad")
                device.linux.ui.run("/usr/bin/leafpad")
                print device.linux.ui.child(text = "leafpad")
                print 'waiting'
                print device.linux.ldtp.waittillguiexist("*baaaa*", 120)
                time.sleep(30)
                #print device.linux.ldtp.appundertest("leafpad")
                #print device.linux.ldtp.wait(5)
                #print device.linux.ldtp.getwindowlist()
                #raw_input()
        print "Time measured = %f" % (tester.timeit.measured,)


