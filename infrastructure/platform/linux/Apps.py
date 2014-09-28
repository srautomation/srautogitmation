from Applications.Browser import Browser
from Applications.Thunderbird import Thunderbird
class Apps(object):
    def __init__(self, rpyc, shell, ui, ip):
        self._rpyc   = rpyc
        self._shell = shell
        self._ui     = ui
        self._ip     = ip 

        self._browser    = None
        self._thuderbird = None

    def start(self):
        self._browser     = Browser(self._shell, self._ip)
        self._thunderbird = Thunderbird(self._rpyc, self._ui)

    def stop(self):
        pass

    @property
    def browser(self):
        return self._browser

    @property
    def thunderbird(self):
        return self._thunderbird




