from sr_automation.platform.android.Android import Android
from sr_automation.platform.android.NetInterfaces import NetInterfaces
from sr_automation.platform.linux.Linux import Linux
from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
from sr_automation.platform.sunriver.applications.SwitchToAndroid.SwitchToAndroid import SwitchToAndroid
from Chroot import Chroot
import rpyc
import time
from selenium import webdriver
from logbook import Logger
log = Logger("Sunriver")
from bunch import Bunch
import os
import subprocess
from sr_tools import helpers

class Sunriver(object):
    def __init__(self):
        try:
            helpers.latest_wifi_adb_connection('read')
            self._device_id = Android.devices().keys()[0]
        except:
            print 'please connect android device for its key'
            helpers.wait_usb_connection()
            self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        #self._desktop = DesktopInYourPocket(self._android)
        #self._linux = self.connect(Chroot(self._android), NetInterfaces(self._android))
	self._linux = self.connect(NetInterfaces(self._android))
        self._switch_to_android =  SwitchToAndroid(self._linux, self._desktop)
        self.start()

    def start(self):
        #self._desktop.start()
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

    def connect(self, interfaces):
        devices = helpers.adb_devices()
	deviceip = helpers.device_ip(devices.ip)
        print deviceip
        helpers.adb_over_wifi(deviceip)
        helpers.wait_for_MHL_connection()
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._desktop = DesktopInYourPocket(self._android)
        log.info("Starting RPyC")
	ssh_command = "ssh -p 2222 BigScreen@%s 'DISPLAY=:0 rpyc_classic.py > /dev/null > /tmp/mylogfile 2>&1 &'"%deviceip
        if not self._desktop.is_desktop_running():#checks if desktop is not already running
            self._desktop.start()
	    log.info("Loading Desktop")
	    for i in range(4):
	        print i
	        time.sleep(1)
        else:
            print 'Desktop is already running'
	os.system(ssh_command)
	log.info("Connecting RPyC: %r" % deviceip)
        flag=0
        while(flag==0):
            try:
                rpyc_user_connection = rpyc.classic.connect(deviceip)
                rpyc_connection = rpyc.classic.connect(deviceip)
                flag=1
            except:
                log.info('rpyc connection refused - retrying rpyc')
                time.sleep(3)
                flag=0
        print 'Connected!'
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection, modules_user=rpyc_user_connection.modules, rpyc_user=rpyc_user_connection)


    @classmethod
    def install(cls):
	os.system('adb remount')
	os.system('adb disable-verity')
	os.system('adb reboot')
	os.system('adb wait-for-device')
	for i in range(20):
		print i
		time.sleep(1)
        os.system("adb shell svc power stayon true")#stay awake on phone
	os.system('adb root')
	time.sleep(5)
	os.system('adb push ~/sr_automation/rc.updates /data/sunriver/fs/limited/etc/rc.d/rc.updates')
	os.system('adb shell chmod 777 /data/sunriver/fs/limited/etc/rc.d/rc.updates')


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
