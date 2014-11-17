class Accessibility(object):
    def __init__(self, rpyc, shell):
        self._shell = shell
        self._rpyc = rpyc

    def start(self):
        self._shell.wait_process_by_short_name("Xorg")
        assert 0 == self._shell.shell("gsettings set org.gnome.desktop.interface toolkit-accessibility true", infrastructure = True).wait()
        assert 0 == self._shell.shell("gconftool-2 -s -t boolean /desktop/gnome/interface/accessibility true", infrastructure = True).wait()

        # IMPORTANT: following line also loads at-spi-bus-launcher:
        self._shell.shell("qdbus org.a11y.Bus /org/a11y/bus org.a11y.Status.IsEnabled", infrastructure = True)

        self._shell.wait_process_by_short_name("at-spi-bus-laun")
        self._shell.cmd("/usr/lib/at-spi2-core/at-spi2-registryd", infrastructure = True)
        self._shell.wait_process_by_short_name("at-spi2-registr")

        # start ldtp
        if not self._shell.is_running_by_short_name("ldtp"):
            self._shell.cmd("/usr/bin/ldtp", infrastructure = True)
            self._shell.wait_process_by_short_name("ldtp")
    
        # fix dogtail bug
        self._rpyc.modules.os.getlogin = lambda: "root"
        self._rpyc.modules.os.environ["USER"] = "root"
   
        # self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)
        #log.info("Connected to ldtp with xmlrpc")

    def stop(self):
        pass
