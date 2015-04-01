from bunch import Bunch
from logbook import Logger
log = Logger("Chroot")

class Chroot(object):
    MOUNTS = [ Bunch(type="ext4",    dev="/dev/block/mmcblk1p1", path="/data/debian")
             , Bunch(type="proc",    dev="proc",                 path="/data/debian/proc")
             , Bunch(type="sysfs",   dev="sysfs",                path="/data/debian/sys")
             , Bunch(options="bind", dev="/dev",                 path="/data/debian/dev")
             , Bunch(type="devpts",  dev="devpts",               path="/data/debian/dev/pts")
             , Bunch(type="tmpfs",   dev="/dev/shm",             path="/data/debian/dev/shm")
            ]
    ENV = { "USER": "root"
          , "DISPLAY": ":0"
          , "GTK_MODULES": "gail:atk-bridge"
          }
    PATH = [ "/usr/local/sbin"
           , "/usr/local/bin"
           , "/usr/sbin"
           , "/usr/bin"
           , "/sbin"
           , "/bin"
           , "/system/xbin"
           ]

    def __init__(self, android):
        self._android = android

    def mounted(self):
        return [l.split(" ")[1] for l in self._android.cmd("shell cat /proc/mounts").stdout.readlines()]

    def all_mounted(self):
        paths = [m.path for m in Chroot.MOUNTS]
        mounted_paths = self.mounted()
        return set(mounted_paths) == set(paths)

    def mount(self):
        _mounted = self.mounted()
        for _mount in Chroot.MOUNTS:
            if _mount.path in _mounted:
                continue
            type    = ["", "-t %s" % _mount.get("type", "")]["type" in _mount]
            options = ["", "-o %s" % _mount.get("options")]["options" in _mount]
            self._android.cmd("shell mount %s %s %s %s" % (type, options, _mount.dev, _mount.path)).wait()

    def run(self, cmdline, shell=True):
        if not self.all_mounted():
            self.mount()
        if shell:
            cmdline = 'su - -c "%s"' % (cmdline)
        env = " ".join(["%s=%s" % (k, v) for (k, v) in Chroot.ENV.iteritems()])
        path = ":".join(Chroot.PATH)
        chroot_cmdline = '%s PATH=%s HOME=/root busybox chroot %s %s' % (env, path, Chroot.MOUNTS[0].path, cmdline)
        log.info(chroot_cmdline)
        return self._android.cmd('shell %s' % chroot_cmdline)

if __name__ == "__main__":
    import sys; sys.path.append("../android")
    from Android import Android
    device_id  = Android.devices().keys()[0]
    android    = Android(device_id)
    chroot     = Chroot(android)
    print chroot.run("ls -la").stdout.read()
