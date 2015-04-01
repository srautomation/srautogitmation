from Shell import Shell
from UI import UI

import rpyc
import time
from logbook import Logger
log = Logger("Linux")

class Linux(object):
    def __init__(self, modules, rpyc=None):
        self._modules = modules
        self._rpyc = rpyc
        self._shell = Shell(self._modules, self._rpyc)

    def __del__(self):
        if self._rpyc is not None:
            self._rpyc.close()

    @classmethod
    def connect(cls, chroot, interfaces):
        log.info("Starting RPyC")
        rpyc_process = chroot.run("rpyc_classic.py", shell=False)
        log.info("Waiting RPyC")
        android = chroot._android
        while (0 == len(android.cmd('shell "netstat | grep :18812 | grep LISTEN"').stdout.read())):
            time.sleep(0.5)
        try:
            iface = interfaces["rndis0"]
        except KeyError, e:
            iface = interfaces["wlan0"]
        log.info("Connecting RPyC: %r" % iface.ip)
        rpyc_connection = rpyc.classic.connect(iface.ip)
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection)

    def start(self):
        self._ui = UI(self._rpyc, self._shell, self._ip)

        self._ui.start()

    def stop(self):
        self._ui.stop()

    @property
    def modules(self):
        return self._modules

    @property
    def shell(self):
        return self._shell

    @property
    def ui(self):
        return self._ui

    def cmd(self, cmdline, *args, **kw):
        return self.shell.cmd(cmdline, *args, **kw)

if __name__ == "__main__":
    import sys; sys.path.append("../android")
    from Android import Android
    from Chroot  import Chroot
    from NetInterfaces import NetInterfaces
    device_id  = Android.devices().keys()[0]
    android    = Android(device_id)

    chroot     = Chroot(android)
    interfaces = NetInterfaces(android)
    linux = Linux.connect(chroot, interfaces)

    print linux.modules.os.listdir("/")
    print linux.cmd("ls -la").stdout.read()

