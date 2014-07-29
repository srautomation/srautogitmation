from gevent import monkey; monkey.patch_all()
from UI import UI
from subprocess import PIPE
import xmlrpclib
import time
import gevent

class Linux(object):
    POLL_DELAY_WAIT_RUNNING = 0.2
    def __init__(self, ip, rpyc_connection):
        self._rpyc = rpyc_connection
        self._ip   = ip
        self._os   = self._rpyc.modules.os
        self._subprocess = self._rpyc.modules.subprocess
        self._processes = {}
        #self._psutil = self._rpyc.modules.psutil
        self._env = {}
        self._env["DISPLAY"]         = ":0.0"
        self._env["GTK_MODULES"]     = "gail:atk-bridge" 
        self._env["XDG_RUNTIME_DIR"] = "/tmp/"
        self._ldtp_process = None
        self._ldtp = None

        
    def cmd(self, cmdline, shell = True, env = None):
        _temp_env = self._os.environ.copy()
        _temp_env.update(self._env)
        if env is not None:
            _temp_env.update(env)
        return self._subprocess.Popen(cmdline, shell = shell, stdout = PIPE, stderr = PIPE, env = _temp_env)

    def is_running(self, pattern):
        return (0 == self.cmd('ps -fe | grep -v grep | grep "%s"' % (pattern,)).wait())

    def wait_running(self, pattern, timeout = None):
        print 'Waiting: %s' % pattern 
        while not self.is_running(pattern): 
            gevent.sleep(Linux.POLL_DELAY_WAIT_RUNNING)
        print 'done waiting'

    def enable_accessibility(self):
        self.wait_running("Xorg")
        assert 0 == self.cmd("gsettings set org.gnome.desktop.interface toolkit-accessibility true").wait()
        assert 0 == self.cmd("gconftool-2 -s -t boolean /desktop/gnome/interface/accessibility true").wait()

        # IMPORTANT: following line also loads at-spi-bus-launcher:
        assert "true" == self.cmd("qdbus org.a11y.Bus /org/a11y/bus org.a11y.Status.IsEnabled").stdout.read().strip()
        self.wait_running("at-spi-bus-launcher")
        #self.wait_running("dbus-launch")
            
    def start(self):
        self.enable_accessibility()
        self._ui_start()

    def stop(self):
        self._ui_stop()

    def _ui_start(self):
        self._ldtp = None
        self._ldtp_start()
        self._dogtail_start()
        self._ui = UI(ldtp = self._ldtp, dogtail = self._dogtail)

    def _ui_stop(self):
        self._ldtp_stop()
        self._dogtail_stop()

    def _ldtp_start(self):
        self._ldtp = None
        #return
        LDTP_PATH = "/usr/bin/ldtp"
        self.wait_running("at-spi-bus-launcher")
        if not self.is_running("/usr/bin/ldtp"):
            self._ldtp_process = self.cmd("/usr/bin/ldtp", shell = False)
            self.wait_running("/usr/bin/ldtp")
        self.wait_running("at-spi2-registryd")
        self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)

    def _ldtp_stop(self):
        self._ldtp_process.kill()

    def _dogtail_start(self):
        self._dogtail = None
        return
        # fix dogtail bug
        self._os.getlogin = lambda: self._rpyc.modules.pwd.getpwuid(self._os.getuid())[0]
        self._dogtail = self._rpyc.modules.dogtail

    def _dogtail_stop(self):
        pass

    @property
    def ui(self):
        return self._ui

    @property
    def ldtp(self):
        return self._ldtp
