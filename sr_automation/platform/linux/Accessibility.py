import time

class Accessibility(object):
    def __init__(self, rpyc, shell):
        self._shell = shell
        self._rpyc = rpyc
        self._process_at_spi_bus_launcher = None
        self._process_at_spi_registryd = None

    def start(self):
        self._shell.wait_process_by_short_name("Xorg")
        assert 0 == self._shell.shell("gsettings set org.gnome.desktop.interface toolkit-accessibility true", infrastructure = True).wait()
        assert 0 == self._shell.shell("gconftool-2 -s -t boolean /desktop/gnome/interface/accessibility true", infrastructure = True).wait()
        
        self._process_at_spi_bus_launcher = self._shell.cmd("/usr/lib/at-spi2-core/at-spi-bus-launcher", infrastructure = True)
        self._shell.wait_process_by_short_name("at-spi-bus-laun")

        self._process_at_spi_registryd = self._shell.cmd("/usr/lib/at-spi2-core/at-spi2-registryd", infrastructure = True)
        self._shell.wait_process_by_short_name("at-spi2-registr")

        # start ldtp
        if not self._shell.is_running_by_short_name("ldtp"):
            self._shell.cmd("/usr/bin/ldtp", infrastructure = True)
            self._shell.wait_process_by_short_name("ldtp")
    
        # fix dogtail bug
        self._rpyc.modules.os.getlogin = lambda: "root"
        self._rpyc.modules.os.environ["USER"] = "root"

    def stop(self):
        pass
        #self._process_at_spi_bus_launcher.kill()
        #self._process_at_spi_registryd.kill()
