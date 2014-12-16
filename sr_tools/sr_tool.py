import baker
import re
import time
from bunch import Bunch
import helpers as H
from subprocess import Popen, PIPE

@baker.command
def devices():
    """Show connected devices"""
    print H.adb_devices()


@baker.command
def project_root():
    """Show project root path"""
    print H.project_root()


@baker.command
def mount_resources():
    """Mount externals directory"""
    pass


@baker.command(params={"device_id": "Device id"})
def mode_wifi(device_id = None):
    """Connect DUT over WIFI, disconnect USB"""
    devices = H.adb_devices()
    if len(devices.usb) == 0:
        return
    if device_id is not None:
        assert device_id in devices.usb
    else:
        device_id = devices.usb[0]
    
    ip = H.device_ip(device_id)
    port = 5555
    Popen(["adb", "tcpip",   "%d" % (port,)]).wait()
    time.sleep(4)
    Popen(["adb", "connect", "%s" % (ip,)]).wait()
    print "Disconnect USB cable..."
    H.wait_usb_disconnection()
    print H.adb_devices()


@baker.command(params={"device_id": "Device id"})
def mode_usb(device_id = None):
    """Connect DUT over USB, disconnect WIFI"""
    devices = H.adb_devices()
    if len(devices.ip) == 0:
        return
    if device_id is not None:
        assert device_id in devices.ip
    else:
        device_id = devices.ip[0]
    
    Popen(["adb", "disconnect"]).wait()
    print "Connect USB cable now..."
    H.wait_usb_connection()
    print H.adb_devices()


APT_PACKAGES = [
    "git",
    "at-spi2-core", "libatk-bridge2.0-0", "libatk-adaptor", "ldtp", 
    "gconf2", "qdbus", 
    "python-dev", "python-pip", "python-pyatspi2", "python-gtk2", "python-gtk2-dev", "python-pil", "python-gobject", "python-gobject-2", 
    "statgrab", "wmctrl",
]
PIP_PACKAGES = ["rpyc", "psutil", "selenium", "chromedriver", "Skype4py"] # "twisted"

@baker.command(params={"device_id": "Device id"})
def install_dut(device_id = None):
    """Prepare DUT for use by automation framework"""
    from sr_automation.Device import Device
    devices = H.adb_devices()
    if device_id is not None: assert device_id in devices
    device = Device(device_id)
    commands = "\n".join([
        "apt-get -y install " + " ".join(APT_PACKAGES),
        "pip install "        + " ".join(PIP_PACKAGES),
        "git clone https://github.com/lorquas/dogtail; cd dogtail; python setup.py install; cd .. ;",
        "ln -s /usr/lib/i386-linux-gnu/gtk-2.0/ /usr/lib/gtk-2.0;", # TODO: validate
    ])
    process = device._chroot_run(commands)
    while True:
        line = process.stdout.readline()
        if not line: break
        print line,
    process.wait()

"""
run from a directory with a .slashrc in it (TODO: fix)
sudo sr_tool run_tests --suite=mail -vvv BasicTests.py
"""
@baker.command(params={
    "path": "Path of test file", 
    "suite": "Suite name",
    "externals": "Path of external resources",})
def run_tests(path=None, suite=None, externals="", *args):
    """Run tests"""
    if ((path is None) and (suite is None)) or ((path is not None) and (suite is not None)):
        return
    import os
    os.environ["PROJECT_ROOT"] = H.project_root()
    os.environ["EXTERNALS"] = externals
    if suite is not None:
        path = os.path.join(os.environ["PROJECT_ROOT"], "sr_tests", suite + "_suite")
    with H.chdir(path):
        os.system("slash run %s" % " ".join(args))

def main():
    baker.run()
