from sr_automation.platform.android.Android import Android
from sr_automation.platform.android.NetInterfaces import NetInterfaces
from sr_automation.platform.linux.Linux import Linux
from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
from Chroot import Chroot
import rpyc
import time

from logbook import Logger
log = Logger("Sunriver")

class Sunriver(object):
    def __init__(self):
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._desktop = DesktopInYourPocket(self._android)
        self._linux = Sunriver.connect(Chroot(self._android), NetInterfaces(self._android))

    @classmethod
    def connect(cls, chroot, interfaces):
        log.info("Starting RPyC")
        rpyc_process = chroot.run("rpyc_classic.py", shell=False)
        log.info("Waiting RPyC")
        android = chroot._android
        while (0 == len(android.cmd('shell "netstat | grep :18812 | grep LISTEN"').stdout.read())):
            time.sleep(0.5)
        try:
            iface = interfaces["rndis0"]
        except KeyError, e:
            iface = interfaces["wlan0"]
        log.info("Connecting RPyC: %r" % iface.ip)
        rpyc_connection = rpyc.classic.connect(iface.ip)
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection)

    @property
    def android(self):
        return self._android

    @property
    def linux(self):
        return self._linux

    @property
    def desktop(self):
        return self._desktop

if __name__ == "__main__":
    sunriver = Sunriver()
    print sunriver
