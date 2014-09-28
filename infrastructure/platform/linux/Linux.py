from Shell import Shell
from UI import UI
from Accessibility import Accessibility
from Apps import Apps

from logbook import Logger
log = Logger("Linux")

class Linux(object):
    def __init__(self, ip, rpyc):
        self._ip   = ip
        self._rpyc = rpyc

        self._shell         = None
        self._accessibility = None
        self._ui            = None
        self._browser       = None
        self._apps          = None

    def start(self):
        self._shell = Shell(self._rpyc)
        self._shell.shell("ln -s /run/shm /dev/shm", infrastructure = True)
        self._accessibility = Accessibility(self._rpyc, self._shell)
        self._ui = UI(self._rpyc, self._shell, self._ip)
        self._apps = Apps(self._rpyc, self._shell, self._ui, self._ip)

        self._shell.start()
        self._accessibility.start()
        self._ui.start()
        self._apps.start()

    def stop(self):
        self._apps.stop()
        self._ui.stop()
        self._accessibility.stop()
        self._shell.stop()

    @property
    def shell(self):
        return self._shell

    @property
    def accessibility(self):
        return self._accessibility

    @property
    def ui(self):
        return self._ui

    @property
    def apps(self):
        return self._apps

    def cmd(self, *args, **kw):
        return self._shell.cmd(*args, **kw)

