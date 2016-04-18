from sr_tools import config
from sr_automation.platform.android.Android import Android
from sr_automation.platform.linux.Linux import Linux
from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
from sr_automation.platform.sunriver.applications.SwitchToAndroid.SwitchToAndroid import SwitchToAndroid
from sr_automation.platform.sunriver.applications.isVNC.VNCInYourPocket import VNCInYourPocket
import rpyc
import time
import socket
import getpass
from logbook import Logger
log = Logger("Sunriver")
import os
from sr_tools import helpers #package containing connection functions

class Sunriver(object):
    def __init__(self):
        os.system('adb devices')#line here for testing certain times device doesnt connect
        helpers.latest_wifi_adb_connection('read')#reads txt file that contains the last ip device connected to pc.
        if len(Android.devices().keys()) > 0:#checks if any device is already connected to pc.
            self._device_id = Android.devices().keys()[0]
        else:
            log.warn('please connect android device to usb for adb connection')
            helpers.wait_usb_connection() 
            self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)#runs android Object
        self._linux = self.connect()#starts connection to linux side of DUT, starts desktop aswell if needed.
        self._switch_to_android =  SwitchToAndroid(self._linux, self._desktop)
        self._vnc_control_pocket = VNCInYourPocket(self._linux)#VNC control app
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
    def vnc(self):
        return self._vnc_control_pocket
    
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

    def rpyc_connect(self, ip, timef=0):#soul purpose of the function is to make RPyC connection persistant
        while True:
            try:
                return rpyc.classic.connect(ip)
            except:
                log.warn('RPyC Connection Refused - Retrying RPyC')
                time.sleep(3)
                timef+=1
                if timef == 8:
                    helpers.ssh_connect(ip)#if connection fails 5 time, ssh settings are reset.

    def connect(self):
        devices = helpers.adb_devices()#device paramater receives all the adb connections of the PC(ip,usb).
        deviceip = helpers.device_ip(devices.ip)#stores the ip connection of DUT if available(could be empty).
        helpers.adb_over_wifi(deviceip)#checks adb over wifi connection, and sets one if not available.
        helpers.wait_for_MHL_connection()#waits until DUT is connected to to an MHL cable
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)#resets android object now surely using adb over WIFI
        self._desktop = DesktopInYourPocket(self._android)#objects containing automatic android control functions
        log.info("Starting RPyC")
        ssh_command = "ssh -p 2222 BigScreen@%s 'DISPLAY=:0 rpyc_classic.py > /dev/null > /tmp/mylogfile 2>&1 &'"%deviceip
        self.start_desktop(self._desktop)#checks if starting desktop is needed
        os.system(ssh_command)#running ssh command that starts RPyC server on DUT side.
        log.info("Connecting RPyC: %r" % deviceip)
        rpyc_connection = self.rpyc_connect(deviceip)#stores RPyC connection making it available to use device modules from pc
        log.info('Connected!')
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection, modules_user=rpyc_connection.modules, rpyc_user=rpyc_connection)

    @classmethod
    def install(cls):
        local_ip = ([(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        username=getpass.getuser()
        import pdb;pdb.set_trace()
        placeholderFile = open(config.get_working_dir() + '/sr-auto-installation-placeholder','r')
        installationFile = open(config.get_working_dir()+ '/sr-auto-installation','w')
        for line in placeholderFile:
            if 'username' in line:
                newline = line.replace('placeholder',local_ip).replace('username',username)
            else:
                newline = line
            installationFile.write(newline) 
        placeholderFile.close()
        installationFile.close()
        #disables verity on device to make file transfer to device possible
        os.system('adb root')
        os.system('adb remount')
        os.system('adb disable-verity')
        os.system('adb reboot')#disable-verity needs reboot
        os.system('adb wait-for-device')
        for i in range(30): print i; time.sleep(1)
        os.system('adb shell svc power stayon true')#stay awake on phone
        os.system('adb root')
        time.sleep(5)
        #problem transerfering srautomation-packages.tar.gz using os.system - may make adb connection offline 
        print 'RUN: adb push ~/sr_automation/srautomation-packages.tar.gz /data/sunriver/fs/limited/media/'
        os.system('adb push ~/sr_automation/sr-auto-installation /data/sunriver/fs/limited/home/BigScreen/')#transfering installation script to dut.
        os.system('adb shell chmod 777 /data/sunriver/fs/limited/home/BigScreen/sr-auto-installation')#changing file permissions.


        
        #=======================================================================
        # print "try to copy zip file"
        # from subprocess import check_output, CalledProcessError
        # try:     
        #     #adb_output = check_output(["adb", "push", "/home/labuser/sr_automation/srautomation-packages.tar.gz" ,"/data/sunriver/fs/limited/media/"])
        #     proc = subprocess.Popen(cmd,shell=True)
        #     print "succeed copy zip file"
        # except CalledProcessError as e:
        #     print e.message
        #=======================================================================
       
        


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
