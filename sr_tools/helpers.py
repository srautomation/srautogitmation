from bunch import Bunch
import subprocess
import re
import time
import operator
import os
from logbook import Logger
log = Logger("connection functions")

#path locations
dut_latest_ip='/usr/local/bin/dut_latest_ip.txt'
adb_devices_string="adb devices"
usb_count="lsusb | wc -l"

def project_root():
    return os.path.split(os.path.abspath(os.path.join(__file__, "..")))[0]

def find_file_location(filename,path):
    for root, dirs, files in os.walk(path):
        if filename in files:
            return os.path.join(root, filename)



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
        log.warn('please connect MHL cable')
        time.sleep(2)
        mhl = subprocess.Popen(["adb", "shell", "cat /sys/class/switch/hdmi/state"], stdout=subprocess.PIPE).stdout.read()

def adb_connection(ip):
    os.system('adb connect %s'%ip)
    time.sleep(2)

def latest_wifi_adb_connection(read_write):
    IP_FILE_NAME = "dut_latest_ip.txt"
    PATH = "/"
    ip_file_path = find_file_location(IP_FILE_NAME, PATH) 
    print ip_file_path
    if read_write == 'read':
        ip_file = open(dut_latest_ip, 'r')
        ip = ip_file.read().strip()
        adb_connection(ip)
    else:
        ip_file = open(dut_latest_ip, 'w')
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
        log.warn("connect phone to usb for ip inspection")
        wait_usb_connection()
        device_ip(device_id)

def adb_over_wifi(deviceip):#Need to inspect option in which no wifi is detected on phone - should appear as None
    devices = adb_devices()
    if len(devices.ip) == 0:
        while len(devices.ip) == 0:
            os.system("adb tcpip 5555")
            time.sleep(5)
            log.info('trying to connect adb over wifi')
            adb_connection(deviceip)
            devices = adb_devices()
        latest_wifi_adb_connection(deviceip)
        log.warn('connection over wifi successful - disconnect device and connect to MHL')
        wait_usb_disconnection()
    else:
        if len(devices.ip) == 1 and len(devices.usb) == 1:
            log.warn('adb over wifi connected - disconnect usb')
            wait_usb_disconnection()
        else:
            log.warn('adb over already wifi connected')

def ssh_connect(ip):
    os.system('adb push /home/labuser/sr_automation/sshd_config /data/sunriver/fs/limited/etc/ssh/')
    os.system('adb reboot')
    os.system('adb wait-for-device')
    print 'connect bluetooth device to DUT - and load sunriver ALT-UP'
    for i in range(10): print i; time.sleep(1)
    os.system('ssh-add')
    os.system('ssh-keygen -f "/home/automation/.ssh/known_hosts" -R [%s]:2222'%ip)
    os.system('ssh-copy-id -p 2222 BigScreen@%s'%ip)

class chdir:
    def __init__(self, path):
        self._path = path
    def __enter__(self):
        self._cwd = os.getcwd()
        os.chdir(self._path)
    def __exit__(self, type, value, traceback):
        os.chdir(self._cwd)
