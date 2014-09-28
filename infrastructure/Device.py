from Resources import Resources
from platform.android import Android
from platform.linux   import Linux
from collections      import namedtuple
import socket
import rpyc
import time
import subprocess

from logbook import Logger
log = Logger("Device")

class Device(object):
    DEFAULT_RPYC_INTERFACE = "wlan0"
    APP_TITLE        = "Intel's Desktop In Your Pocket"
    APP_START_BUTTON = "Start Desktop OS"
    APP_STOP_BUTTON  = "Kill Desktop OS"

    def __init__(self, device_id = None, linux_ip = None):
        if device_id is None:
            device_id = subprocess.Popen("adb devices | sed 1d | awk {'print $1'}", shell = True, stdout = subprocess.PIPE).stdout.read().strip()
            log.info("DEVICE ID = %s" % device_id)

        self._device_id = device_id
        self._linux_ip = linux_ip
        self._rpyc_process = None
        self._rpyc_connection = None
        self._android = None
        self._resources = None

    #---------------------------------------------------------------------------------------
    # Setup chrooted Linux on real device

    _MOUNTS = [
            {"type": "ext4",    "dev": "/dev/block/mmcblk1p1", "path": "/data/debian"},
            {"type": "proc",    "dev": "proc",                 "path": "/data/debian/proc"},
            {"type": "sysfs",   "dev": "sysfs",                "path": "/data/debian/sys"},
            {"options": "bind", "dev": "/dev",                 "path": "/data/debian/dev"},
            {"type": "devpts",  "dev": "devpts",               "path": "/data/debian/dev/pts"},
            ]
    def _try_setup_mounts(self):
        mounted = [l.split(" ")[1] for l in self.android.adb.cmd("shell cat /proc/mounts").stdout.readlines()]
        for mount in Device._MOUNTS:
            if mount["path"] in mounted:
                continue

            type    = ["", "-t %s" % mount.get("type", "")]["type" in mount]
            options = ["", "-o %s" % mount.get("options")]["opions" in mount]
            self.android.adb.cmd("shell mount %s %s %s %s" % (type, options, mount["dev"], mount["path"]))


    def _chroot_run(self, cmdline, shell = True):
        if self._android is None:
            self._android = Android.Android(self._device_id)
        self._try_setup_mounts()
        chroot_path = ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "bin"]
        if shell is True:
            command = 'su - -c "%s"' % (cmdline)
        else:
            command = cmdline
        chroot_cmdline = 'USER=root DISPLAY=:0 GTK_MODULES=gail:atk-bridge PATH=%s HOME=/root /system/xbin/chroot %s %s' % (':'.join(chroot_path), Device._MOUNTS[0]["path"], command)
        return self.android.adb.cmd("shell " + chroot_cmdline)

    def _is_rpyc_running(self):
        return (0 < len(self.android.adb.cmd('shell "cat /proc/*/stat 2>/dev/null | grep rpyc_classic.py"').stdout.read()))

    def _is_rpyc_listening(self):
        return (0 < len(self.android.adb.cmd('shell "netstat | grep 0.0.0.0:18812 | grep LISTEN"').stdout.read()))

    def _start_connect_rpyc(self):
        if (not self._is_rpyc_running()):
            log.info("RPyC start")
            self._rpyc_process = self._chroot_run("rpyc_classic.py", shell = False)
        while (not self._is_rpyc_running()):
            time.sleep(0.01)
        while (not self._is_rpyc_listening()):
            time.sleep(0.01)
        time.sleep(0.5)
        ip = self.android.interfaces[Device.DEFAULT_RPYC_INTERFACE].ip
        log.info("RPyC connect")
        rpyc_connection = rpyc.classic.connect(ip)
        return (ip, rpyc_connection)
    #---------------------------------------------------------------------------------------

    def desktop_start(self):
        self.android.ui.wakeup()
        self.android.cmd("shell am start -n com.intel.desktopinyourpocket/.MainActivity")
        #self.android.cmd("shell su -/data/data/com.intel.desktopinyourpocket/files/startDesktop.tablet.bash")
        self.android.ui(text = Device.APP_TITLE).wait.exists()
        time.sleep(1.5)
        self.android.ui.press.menu()
        self.android.ui(text = Device.APP_START_BUTTON).wait.exists()
        self.android.ui(text = Device.APP_START_BUTTON).click()
        self.android.ui.press.home()

    def desktop_stop(self):
        #self.android.cmd("shell /data/data/com.intel.desktopinyourpocket/files/stopDesktop.tablet.bash")
        self.android.cmd("shell am start -n com.intel.desktopinyourpocket/.MainActivity")
        self.android.ui(text = Device.APP_TITLE).wait.exists()
        time.sleep(1.5)
        self.android.ui.press.menu()
        self.android.ui(text = Device.APP_STOP_BUTTON).wait.exists()
        self.android.ui(text = Device.APP_STOP_BUTTON).click()
        self.android.ui.press.home()
        self.android.cmd("shell am force-stop com.intel.desktopinyourpocket")

    def start(self):
        if self._android is None:
            self._android = Android.Android(self._device_id)
        self._android.start()
        self.desktop_start()
        if self._linux_ip is None:
            self._linux_ip, self._rpyc_connection = self._start_connect_rpyc()
        else:
            self._rpyc_connection = rpyc.classic.connect(self._linux_ip)
        log.info("Linux IP = %s" % (self._linux_ip,))
        self._resources = Resources(self.android.adb)
        self._linux = Linux.Linux(self._linux_ip, self._rpyc_connection, self)
        self._linux.start()

    def stop(self):
        self.desktop_stop()
        self._linux.stop()
        self._android.stop()

    def __enter__(self):
        self.start()
        return self
        
    def __exit__(self, type, value, traceback):
        self.stop()
    
    @property
    def android(self):
        return self._android

    @property
    def linux(self):
        return self._linux

    @property
    def resources(self):
        return self._resources
