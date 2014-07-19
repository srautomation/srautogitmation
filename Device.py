from gevent import monkey; monkey.patch_all()
from gevent import Timeout
from platform.android import Android
from platform.linux   import Linux
from collections      import namedtuple
import rpyc
import time
class Device(object):
    DEFAULT_RPYC_INTERFACE = "wlan0"

    def __init__(self, device_id, rpyc_connection = None):
        self._device_id = device_id
        self._rpyc_connection = rpyc_connection

    #---------------------------------------------------------------------------------------
    # Setup chrooted Linux on real device

    _MOUNTS = [
            {"type": "ext4",    "dev": "/dev/block/mmcblk1p1", "path": "/data/debian"},
            {"type": "proc",    "dev": "proc",                 "path": "/data/debian/proc"},
            {"type": "sysfs",   "dev": "sysfs",                "path": "/data/debian/sysfs"},
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
            time.sleep(1)

    def _chroot_run(self, cmdline):
        self._try_setup_mounts()
        chroot_path = ["/usr/local/sbin", "/usr/local/bin", "/usr/sbin", "/usr/bin", "/sbin", "bin"]
        chroot_cmdline = 'DISPLAY=:0 GTK_MODULES=gail:atk-bridge PATH=%s HOME=/root /system/xbin/chroot %s su - -c "%s"' % (':'.join(chroot_path), Device._MOUNTS[0]["path"], cmdline)
        return self.android.adb.cmd("shell " + chroot_cmdline)

    def _try_install_rpyc(self):
        self._chroot_run("apt-get install -y python-pip")
        self._chroot_run("pip install rpyc")
    
    def _start_connect_rpyc(self):
        if (len(self._chroot_run("ps -a | grep rpyc_classic.py").stdout.read()) == 0):
            self._try_install_rpyc()
            self._chroot_run("rpyc_classic.py")
        ip = self.android.interfaces[Device.DEFAULT_RPYC_INTERFACE].ip
        print ip
        time.sleep(2)
        rpyc_connection = rpyc.classic.connect(ip)
        return (ip, rpyc_connection)
    #---------------------------------------------------------------------------------------

    def desktop_start(self):
        self.android.cmd("shell am start -n com.intel.desktopinyourpocket/.MainActivity")
        #self.android.cmd("shell su -/data/data/com.intel.desktopinyourpocket/files/startDesktop.tablet.bash")

    def desktop_stop(self):
        #self.android.cmd("shell /data/data/com.intel.desktopinyourpocket/files/stopDesktop.tablet.bash")
        self.android.cmd("shell am force-stop com.intel.desktopinyourpocket")

    def start(self):
        self._android = Android.Android(self._device_id)
        self._android.adb.cmd("root")
        self.desktop_start()
        if self._rpyc_connection is None:
            self._ip, self._rpyc_connection = self._start_connect_rpyc()
        self._linux = Linux.Linux(self._ip, self._rpyc_connection)

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
        with Timeout(10) as timeout:
            print device.linux.cmd("uname -a").stdout.read()
            print device.linux.ldtp.launchapp("libreoffice")
            time.sleep(40)
            print device.linux.ldtp.getwindowlist()
            raw_input()


