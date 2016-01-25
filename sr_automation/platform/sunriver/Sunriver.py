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

class Sunriver(object):
    def __init__(self):
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._desktop = DesktopInYourPocket(self._android)
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

	# need to establish ssh connection after ping from android
	# then run rpyc server on desktop
	# then run automation
  # def connect(self, chroot, interfaces):
    def connect(self, interfaces):
	proc = subprocess.Popen(["adb devices"], stdout=subprocess.PIPE, shell=True)
	wifi = str(proc.communicate())
	if wifi.find('192.168.1') == -1:
        	os.system("adb tcpip 5555")
		time.sleep(5)
		proc = subprocess.Popen(["adb shell ifconfig wlan0 | cut -d 'm' -f1 | cut -d ' ' -f3"], stdout=subprocess.PIPE, shell=True)
		(device_ip, err) = proc.communicate()
		print device_ip
		time.sleep(5)
		os.system("adb connect %s"%device_ip)
		print "You should now disconnect your device"
	else:
		proc = subprocess.Popen(["adb shell ifconfig wlan0 | cut -d 'm' -f1 | cut -d ' ' -f3"], stdout=subprocess.PIPE, shell=True)
                (device_ip, err) = proc.communicate()
                print device_ip
        os.system("adb shell svc power stayon true")#stay awake on phone
	device_ip = device_ip.strip()
        log.info("Starting RPyC")
	#need to edit keys in order to enter automatically
	ssh_command = "ssh -p 2222 BigScreen@%s 'DISPLAY=:0 rpyc_classic.py > /dev/null > /tmp/mylogfile 2>&1 &'"%device_ip
        self._desktop.start()
	log.info("Loading Desktop")
	for i in range(4):
		print i
		time.sleep(1)	
	os.system(ssh_command)
	log.info("Connecting RPyC: %r" % device_ip)
        flag=0
        while(flag==0):
            try:
                rpyc_user_connection = rpyc.classic.connect(device_ip)
                rpyc_connection = rpyc.classic.connect(device_ip)
                flag=1
            except:
                log.info('rpyc connection refused')
                time.sleep(3)
                log.info('retrying rpyc')
                flag=0
        print 'Connected!'
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection, modules_user=rpyc_user_connection.modules, rpyc_user=rpyc_user_connection)


   #def install(cls, chroot):
    @classmethod
    def install(cls):
	os.system('adb remount')
	os.system('adb disable-verity')
	os.system('adb reboot')
	os.system('adb wait-for-device')
	for i in range(20):
		print i
		time.sleep(1)
	os.system('adb root')
	time.sleep(5)
	os.system('adb push ~/sr_automation/rc.updates /data/sunriver/fs/limited/etc/rc.d/rc.updates')
	os.system('adb shell chmod 777 /data/sunriver/fs/limited/etc/rc.d/rc.updates')

#      APT_PACKAGES = [ "git"
 #                     , "at-spi2-core"
#                      , "libatk-bridge2.0-0"
#                      , "libatk-adaptor"
#                      , "gconf2"
#                      , "python-dev"
#                      , "python-pip"
#                      , "python-pyatspi2"
#                      , "python-gtk3"
#                      , "python-gtk3-dev"
#                      , "python-pil"
#                      , "python-gobject"
#                      , "python-gobject-2"
#                      , "statgrab"
#                      , "wmctrl"
#                      , "lsof"
#                      , "libxml2-dev"
#                      , "libxslt1-dev"
#                      , "gcc"
#                      ]
#       PIP_PACKAGES = [ "rpyc"
#                      , "psutil"
#                      , "selenium"
#                      , "chromedriver_installer"
#                      , "Skype4py"
#                      , "lxml"
#                      , "caldav"
#                      , "pycarddav"
#                      , "icalendar"
#                      ]

#       commands = [  "apt-get update"
#       	    , "apt-get -y install {}".format(" ".join(APT_PACKAGES))
#                   , "pip install {}".format(" ".join(PIP_PACKAGES))
#                   , "git config --global http.sslVerify false; git clone https://git.fedorahosted.org/git/dogtail.git; cd dogtail; python setup.py install; cd .. ;"
#                   , "ln -s /usr/lib/i386-linux-gnu/gtk-2.0/ /usr/lib/gtk-2.0;", # TODO: validate
#                   ]

#       for command in commands:
#           process = chroot.run(command)
#           while True:
#           	line = process.stdout.readline()
#           	if not line: break
#           	print line,
#           process.wait()

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
