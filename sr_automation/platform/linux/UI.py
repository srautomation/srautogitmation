import xmlrpclib
from logbook import Logger
log = Logger("LinuxUI")

class UI(object):
    def __init__(self, shell):
        self._shell = shell
        self._modules = shell._modules
        self._modules_user = shell._modules_user

    def _start_at_spi(self):
        log.info("Starting AT-SPI")
        assert 0 == self._shell.shell("gsettings set org.gnome.desktop.interface toolkit-accessibility true", infrastructure=True).wait()
        assert 0 == self._shell.shell("gconftool-2 -s -t boolean /desktop/gnome/interface/accessibility true", infrastructure=True).wait()
        if not self._shell.is_running("at-spi-bus-launcher"):
            log.info("Starting at-spi-bus-launcher")
            self._process_at_spi_bus_launcher = self._shell.cmd('su labuser -c "/usr/lib/at-spi2-core/at-spi-bus-launcher"', infrastructure=True)
            self._shell.wait_process_by_short_name("at-spi-bus-laun")
        if not self._shell.is_running("at-spi2-registryd"):
            log.info("Starting at-spi2-registryd")
            self._process_at_spi_registryd = self._shell.cmd('su labuser -c "/usr/lib/at-spi2-core/at-spi2-registryd"', infrastructure=True)
            self._shell.wait_process_by_short_name("at-spi2-registr")

    def _start_dogtail(self):
        #self._modules.os.getlogin = lambda: "root"
        #self._modules.os.environ["USER"] = "root"
        self._dogtail = self._modules_user.dogtail
        log.info("Starting Dogtail")

    def start(self):
        self._start_at_spi()
        self._start_dogtail()

    def stop(self):
        pass

    @property
    def dogtail(self):
        return self._dogtail

if __name__ == "__main__":
    import sys
    sys.path.append("../android")
    sys.path.append("../sunriver")
    sys.path.append("../sunriver/applications/DesktopInYourPocket")
    import time
    from Android import Android
    from Sunriver import Sunriver
    from Chroot  import Chroot
    from NetInterfaces import NetInterfaces
    from DesktopInYourPocket import DesktopInYourPocket
    from Linux import Linux
    from Shell import Shell

    device_id  = Android.devices().keys()[0]
    android    = Android(device_id)
    desktop    = DesktopInYourPocket(android)
    desktop.start()

    chroot     = Chroot(android)
    interfaces = NetInterfaces(android)
    linux = Sunriver.connect(chroot, interfaces)
    shell = Shell(linux.modules, linux._rpyc)
    ui    = UI(shell)
    ui.start()

    shell.cmd("leafpad")
    time.sleep(2)
    leafpad = ui.dogtail.tree.root.child("(Untitled)")
    print leafpad

