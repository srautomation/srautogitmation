from UI import UI
from Resources import Resources
from Applications.Browser import Browser
from Applications.Thunderbird import Thunderbird
from subprocess import PIPE
import xmlrpclib
import time

from logbook import Logger
log = Logger("Linux")

class Linux(object):
    POLL_DELAY_WAIT_UNTIL_RUNNING = 0.2
    def __init__(self, ip, rpyc_connection):
        self._rpyc = rpyc_connection
        self._ip   = ip
        self._os   = self._rpyc.modules.os
        self._subprocess = self._rpyc.modules.subprocess
        self._processes = {}
        #self._psutil = self._rpyc.modules.psutil
        self._env = {}
        self._env["PATH"] = "/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin"
        self._env["USER"] = "root"
        self._env["DISPLAY"] = ":0.0"
        self._env["GTK_MODULES"] = "gail:atk-bridge"
        self._env["XDG_RUNTIME_DIR"] = "/tmp/"
        self._ldtp_process = None
        self._ldtp = None
        self._dogtail = None
        self._ui = None
        self._resources = None
        self._browser = None
        self._thunderbird = None
        
    def cmd(self, cmdline, shell = True, env = None):
        _temp_env = self._os.environ.copy()
        _temp_env.update(self._env)
        if env is not None:
            _temp_env.update(env)
        return self._subprocess.Popen(cmdline, shell = shell, stdout = PIPE, stderr = PIPE, env = _temp_env)

    def is_running(self, pattern):
        return (0 == self.cmd('ps -fe | grep -v grep | grep "%s"' % (pattern,)).wait())

    def wait_until_running(self, pattern, timeout = None):
        log.info("Waiting: %s" % pattern)
        while not self.is_running(pattern): 
            time.sleep(Linux.POLL_DELAY_WAIT_UNTIL_RUNNING)

    def enable_accessibility(self):
        self.wait_until_running("Xorg")
        assert 0 == self.cmd("gsettings set org.gnome.desktop.interface toolkit-accessibility true").wait()
        assert 0 == self.cmd("gconftool-2 -s -t boolean /desktop/gnome/interface/accessibility true").wait()

        # IMPORTANT: following line also loads at-spi-bus-launcher:
        assert "true" == self.cmd("qdbus org.a11y.Bus /org/a11y/bus org.a11y.Status.IsEnabled").stdout.read().strip()
        #self.cmd("/usr/lib/at-spi2-core/at-spi-bus-launcher")
        self.wait_until_running("at-spi-bus-launcher")
        self.cmd("/usr/lib/at-spi2-core/at-spi2-registryd", shell = False)
        self.wait_until_running("/usr/lib/at-spi2-core/at-spi2-registryd")

    def _fix_dev_shm(self):
        self.cmd("ln -s /run/shm /dev/shm")
            
    def start(self):
        self.enable_accessibility()
        self._fix_dev_shm()
        self._ui_start()
        self._resources = Resources(self._rpyc, self.cmd)
        self._browser = Browser(self.cmd, self._ip)
        self._thunderbird = Thunderbird(self._rpyc, self.ui)

    def stop(self):
        self._ui_stop()
        self._browser.stop()

    def _ui_start(self):
        self._ldtp_start()
        self._dogtail_start()
        self._ui = UI(ldtp = self._ldtp, dogtail = self._dogtail)

    def _ui_stop(self):
        self._ldtp_stop()
        self._dogtail_stop()

    def _ldtp_start(self):
        LDTP_PATH = "/usr/bin/ldtp"
        if not self.is_running(LDTP_PATH):
            self._ldtp_process = self.cmd(LDTP_PATH, shell = False)
            self.wait_until_running(LDTP_PATH)
        self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)
        log.info("Connected to ldtp with xmlrpc")

    def _ldtp_stop(self):
        pass

    def _dogtail_start(self):
        # fix dogtail bug
        self._rpyc.modules.os.getlogin = lambda: "root"
        self._rpyc.modules.os.environ["USER"] = "root"
        self._dogtail = self._rpyc.modules.dogtail
        log.info("Got Dogtail module from RPyC")

    def _dogtail_stop(self):
        pass

    @property
    def ui(self):
        return self._ui

    @property
    def resources(self):
        return self._resources

    @property
    def browser(self):
        return self._browser

    @property
    def thunderbird(self):
        return self._thunderbird
