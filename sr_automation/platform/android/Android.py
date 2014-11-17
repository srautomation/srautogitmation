from Battery import Battery
from Activities import Activities
from Processes import Processes
from NetInterfaces import NetInterfaces
import uiautomator

from logbook import Logger
log = Logger("Android")

class Android(object):
    def __init__(self, device_id):
        self._device_id = device_id
        self._ui = uiautomator.Device(serial = self._device_id)
        self._adb = self._ui.server.adb
        self.adb.cmd("root").wait()
        self.adb.cmd("wait-for-device").wait()
        self._battery = Battery(self._adb)
        self._processes = Processes(self._adb)
        self._activities = Activities(self._adb)
        self._interfaces = NetInterfaces(self._adb)

    def start(self):
        pass

    def stop(self):
        pass

    @property
    def adb(self):
        return self._adb

    @property
    def ui(self):
        return self._ui

    @property
    def battery(self):
        return self._battery

    @property
    def processes(self):
        return self._processes

    @property
    def activities(self):
        return self._activities

    @property
    def interfaces(self):
        return self._interfaces

    def cmd(self, cmdline):
        return self.adb.cmd(cmdline)
