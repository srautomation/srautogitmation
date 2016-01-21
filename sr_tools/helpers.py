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

def adb_devices():
    text = subprocess.Popen(["adb", "devices"], stdout=subprocess.PIPE).stdout.read()
    ids = re.compile("^([^\s]+)\s+device", re.MULTILINE).findall(text)
    usb = [_id for _id in ids if not device_id_is_ip(_id)]
    ip  = [_id for _id in ids if device_id_is_ip(_id)]
    return Bunch(usb=usb, ip=ip)

def device_ip(device_id):
    if device_id_is_ip(device_id):
        return device_id.split(":")[0]
    text = subprocess.Popen(["adb", "shell", "netcfg | grep wlan0"], stdout=subprocess.PIPE).stdout.read()
    ip = re.compile("^\s*wlan0\s+UP\s+(.+)/.*$").findall(text)[0] 
    return ip

class chdir:
    def __init__(self, path):
        self._path = path
    def __enter__(self):
        self._cwd = os.getcwd()
        os.chdir(self._path)
    def __exit__(self, type, value, traceback):
        os.chdir(self._cwd)
