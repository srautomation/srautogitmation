from platform.android import Android
from platform.linux   import Linux
from collections      import namedtuple
import socket
import rpyc
import time

from logbook import Logger
log = Logger("Device")

class Device(object):
    DEFAULT_RPYC_INTERFACE = "wlan0"
    APP_TITLE        = "Intel's Desktop In Your Pocket"
    APP_START_BUTTON = "Start Desktop OS"
    APP_STOP_BUTTON  = "Kill Desktop OS"

    def __init__(self, device_id, linux_ip = None):
        self._device_id = device_id
        self._linux_ip = linux_ip
        self._rpyc_process = None
        self._rpyc_connection = None

    #---------------------------------------------------------------------------------------
    # Setup chrooted Linux on real device

    _MOUNTS = [
            {"type": "ext4",    "dev": "/dev/block/mmcblk1p1", "path": "/data/debian"},
            {"type": "proc",    "dev": "proc",                 "path": "/data/debian/proc"},
            {"type": "sysfs",   "dev": "sysfs",                "path": "/data/debian/sys"},
            {"options": "bind", "dev": "/dev",                 "path": "/data/debian/dev"},
            {"type": "devpts",  "dev": "devpts",               "path": "/data/debian/devpts"},
            ]
    def _try_setup_mounts(self):
        mounted = [l.split(" ")[1] for l in self.android.adb.cmd("shell cat /proc/mounts").stdout.readlines()]
        for mount in Device._MOUNTS:
            if mount["path"] in mounted:
                continue

            type    = ["", "-t %s" % mount.get("type", "")]["type" in mount]
            options = ["", "-o %s" % mount.get("options")]["options" in mount]
            self.android.adb.cmd("shell mount %s %s %s %s" % (type, options, mount["dev"], mount["path"]))

    def _chroot_run(self, cmdline, shell = True):
        self._try_setup_mounts()
        chroot_path = ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "bin"]
        if shell is True:
            command = 'su - -c "%s"' % (cmdline)
        else:
            command = cmdline
        chroot_cmdline = 'USER=root DISPLAY=:0 GTK_MODULES=gail:atk-bridge PATH=%s HOME=/root /system/xbin/chroot %s %s' % (':'.join(chroot_path), Device._MOUNTS[0]["path"], command)
        return self.android.adb.cmd("shell " + chroot_cmdline)

    def _wait_rpyc_port(self, address):
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((address, 18812))
                s.close()
                break
            except socket.error, e:
                continue

    def _start_connect_rpyc(self):
        if (len(self._chroot_run("ps -a | grep -v grep | grep rpyc_classic.py").stdout.read()) == 0):
            log.info("RPyC start")
            self._rpyc_process = self._chroot_run("rpyc_classic.py", shell = False)
        ip = self.android.interfaces[Device.DEFAULT_RPYC_INTERFACE].ip
        self._wait_rpyc_port(ip) 
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
        self._android = Android.Android(self._device_id)
        self.desktop_start()
        if self._linux_ip is None:
            self._linux_ip, self._rpyc_connection = self._start_connect_rpyc()
        else:
            self._rpyc_connection = rpyc.classic.connect(self._linux_ip)
        log.info("Linux IP = %s" % (self._linux_ip,))
        self._linux = Linux.Linux(self._linux_ip, self._rpyc_connection)
        self._linux.start()

    def stop(self):
        self.desktop_stop()

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

if __name__ == "__main__":
    device_serial = "MedfieldB60440E1"
    with Device(device_serial) as device:
        with Timeout(15) as timeout:
            print device.linux.cmd("uname -a").stdout.read()
            #time.sleep(40)
            #print device.linux.ldtp.launchapp("leafpad")
            device.linux.ui.run("/usr/bin/leafpad")
            print device.linux.ui.child(text = "leafpad")
            print 'waiting'
            print device.linux.ldtp.waittillguiexist("*baaaa*", 120)
            time.sleep(30)
            #print device.linux.ldtp.appundertest("leafpad")
            #print device.linux.ldtp.wait(5)
            #print device.linux.ldtp.getwindowlist()
            #raw_input()


