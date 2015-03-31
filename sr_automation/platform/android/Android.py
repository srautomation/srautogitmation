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
        RETRIES = 3
        for i in xrange(RETRIES):
            try:
                self.adb.cmd("wait-for-device").wait()
            except EnvironmentError, e:
                time.sleep(1)
                continue
            break
        self._sl4a = None

    @classmethod
    def devices(cls):
        return uiautomator.Adb().devices()

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

    def cmd(self, cmdline):
        return self.adb.cmd(cmdline)

if __name__ == "__main__":
    device_id  = Android.devices().keys()[0]
    android    = Android(device_id)
    print device_id
    print android.cmd("shell ls").stdout.read()
