from Battery import Battery
from Activities import Activities
from Processes import Processes
from NetInterfaces import NetInterfaces
import uiautomator
import sl4a
import time

from logbook import Logger
log = Logger("Android")

class Android(object):
    SL4A_PORT = 23456
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
        self._sl4a = None

    def start_sl4a(self):
        self.adb.cmd("shell", "am", "start", "-a", "com.googlecode.android_scripting.action.LAUNCH_SERVER", 
                      "-n", "com.googlecode.android_scripting/.activity.ScriptingLayerServiceLauncher", 
                      "--ei", "com.googlecode.android_scripting.extra.USE_SERVICE_PORT", str(Android.SL4A_PORT))
        time.sleep(2)
        self.adb.forward(Android.SL4A_PORT, Android.SL4A_PORT)
        self._sl4a = sl4a.Android(("localhost", Android.SL4A_PORT))

    def stop_sl4a(self):
        pass

    def start(self):
        pass
        #self.start_sl4a()

    def stop(self):
        pass
        #self.stop_sl4a()

    @property
    def adb(self):
        return self._adb

    @property
    def ui(self):
        return self._ui

    @property
    def sl4a(self):
        return self._sl4a

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
