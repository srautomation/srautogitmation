from bunch import Bunch
import subprocess
import re
import time
import operator
import os

def project_root():
    return os.path.split(os.path.abspath(os.path.join(__file__, "..")))[0]

def device_id_is_ip(device_id):
    return ":" in device_id

def usb_count():
    return int(subprocess.Popen("lsusb | wc -l", shell=True, stdout=subprocess.PIPE).stdout.read())

def usb_wifi_count():
    str_adb_devices = len(subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE).stdout.read())
    if str_adb_devices < 60:
        return True

def _wait_usb(operator):
    count = usb_count()
    while (operator(count, usb_count())):
        time.sleep(0.1)

def wait_usb_disconnection():
    _wait_usb(operator.le)
    time.sleep(1)

def wait_usb_connection():
    _wait_usb(operator.ge)
    time.sleep(1)

def wait_for_MHL_connection():
    mhl = subprocess.Popen(["adb", "shell", "cat /sys/class/switch/hdmi/state"], stdout=subprocess.PIPE).stdout.read()
    while mhl[0] != '1':
        print 'please connect MHL cable'
        time.sleep(2)
        mhl = subprocess.Popen(["adb", "shell", "cat /sys/class/switch/hdmi/state"], stdout=subprocess.PIPE).stdout.read()

def latest_wifi_adb_connection(read_write):
    if read_write == 'read':
        ip_file = open('/home/automation/sr_automation/sr_tools/dut_latest_ip.txt', 'r')
        ip = ip_file.read().strip()
        os.system("adb connect %s"%ip)
        time.sleep(3)
    else:
        ip_file = open('/home/automation/sr_automation/sr_tools/dut_latest_ip.txt', 'w')
        ip = ip_file.write(read_write)
    ip_file.close()

def adb_devices():
    text = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE).stdout.read()
    ids = re.compile("^([^\s]+)\s+device", re.MULTILINE).findall(text)
    usb = [_id for _id in ids if not device_id_is_ip(_id)]
    ip  = [_id for _id in ids if device_id_is_ip(_id)]
    return Bunch(usb=usb, ip=ip)

def device_ip(device_id):
    try:
        if len(device_id) != 0:
            if device_id_is_ip(device_id[0]):
                return device_id[0].split(":")[0] 
        text = subprocess.Popen(["adb", "shell", "netcfg | grep wlan0"], stdout=subprocess.PIPE).stdout.read()
        ip = re.compile("^\s*wlan0\s+UP\s+(.+)/.*$").findall(text)[0] 
        return ip
    except:
        print "connect phone to usb for ip inspection"
        wait_usb_connection()
        device_ip(device_id)

def adb_over_wifi(deviceip):
    devices = adb_devices()
    if len(devices.ip) == 0:
        os.system("adb tcpip 5555")
        time.sleep(5)
        while len(devices.ip) == 0:
            print 'trying to connect adb over wifi'
            os.system("adb connect %s"%deviceip)
            time.sleep(2)
            devices = adb_devices()
        latest_wifi_adb_connection(deviceip)
        print 'connection over wifi successful - disconnect device and connect to MHL'
        wait_usb_disconnection()
    else:
        if len(devices.ip) == 1 and len(devices.usb) == 1:
            print 'adb over wifi connected - disconnect usb'
            wait_usb_disconnection()
        else:
            print 'adb over wifi connected'
        

class chdir:
    def __init__(self, path):
        self._path = path
    def __enter__(self):
        self._cwd = os.getcwd()
        os.chdir(self._path)
    def __exit__(self, type, value, traceback):
        os.chdir(self._cwd)
