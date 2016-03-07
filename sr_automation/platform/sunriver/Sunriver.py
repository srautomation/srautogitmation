from sr_automation.platform.android.Android import Android
from sr_automation.platform.linux.Linux import Linux
from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
from sr_automation.platform.sunriver.applications.SwitchToAndroid.SwitchToAndroid import SwitchToAndroid
import rpyc
import time
from logbook import Logger
log = Logger("Sunriver")
import os
from sr_tools import helpers #package containing helping functions
import subprocess

class Sunriver(object):
    def __init__(self):
        helpers.latest_wifi_adb_connection('read')
        if len(Android.devices().keys()) > 0:
            self._device_id = Android.devices().keys()[0]
        else:
            log.warn('please connect android device to usb for adb connection')
            helpers.wait_usb_connection()
            self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._linux = self.connect()
        self._switch_to_android =  SwitchToAndroid(self._linux, self._desktop)
        self.start()

    def start(self):
        self._linux.start()

    def stop(self):
        self._switch_to_android.switch()
        self.android.ui.press.home()

    @property
    def android(self):
        return self._android

    @property
    def linux(self):
        return self._linux

    @property
    def desktop(self):
        return self._desktop

    @property
    def switch_to_android(self):
        return self._switch_to_android

    def start_desktop(self, desktop):
        if not desktop.is_desktop_running():#checks if desktop is not already running
            desktop.start()
            log.warn("Loading Desktop")
            for i in range(4): print i; time.sleep(1)
        else:
            log.info('Desktop is already running')

    def rpyc_connect(self, ip):
        timef=0
        while True:
            try:
                return rpyc.classic.connect(ip)
            except:
                log.warn('RPyC Connection Refused - Retrying RPyC')
                time.sleep(3)
                timef+=1
                if timef == 5:
                    helpers.ssh_connect(ip)

    def connect(self):
        devices = helpers.adb_devices()
        deviceip = helpers.device_ip(devices.ip)
        print deviceip
        helpers.adb_over_wifi(deviceip)
        helpers.wait_for_MHL_connection()
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._desktop = DesktopInYourPocket(self._android)
        log.warn("Starting RPyC")
        ssh_command = "ssh -p 2222 BigScreen@%s 'DISPLAY=:0 rpyc_classic.py > /dev/null > /tmp/mylogfile 2>&1 &'"%deviceip
        self.start_desktop(self._desktop)
        os.system(ssh_command)
        log.info("Connecting RPyC: %r" % deviceip)
        rpyc_connection = self.rpyc_connect(deviceip)
        log.warn('Connected!')
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection, modules_user=rpyc_connection.modules, rpyc_user=rpyc_connection)

    @classmethod
    def install(cls):
        os.system('adb root')
        os.system('adb remount')
        os.system('adb disable-verity')
        os.system('adb reboot')
        os.system('adb wait-for-device')
        for i in range(30): print i; time.sleep(1)
        os.system('adb shell svc power stayon true')#stay awake on phone
        os.system('adb root')
        time.sleep(5)
        print 'RUN: adb push ~/sr_automation/srautomation-packages.tar.gz /data/sunriver/fs/limited/media/'
        os.system('adb push ~/sr_automation/sr-auto-installation /data/sunriver/fs/limited/home/BigScreen/')
        os.system('adb shell chmod 777 /data/sunriver/fs/limited/home/BigScreen/sr-auto-installation')


if __name__ == "__main__":
    import baker

    @baker.command
    def install():
        device_id = Android.devices().keys()[0]
        android = Android(device_id)
        Sunriver.install()

    @baker.command
    def test():
    	sunriver = Sunriver()
        print sunriver

    baker.run()
