from logbook import Logger
log = Logger("VNCInYourPocket")

class VNCInYourPocket(object):
    def __init__(self, linux):
        self._linux = linux

    def isVNCOpen(self):
        return self._linux.shell.is_running_by_short_name('vnc')

    def OpenVnc(self):
        log.info('Opening VNC')
        if not self.isVNCOpen():
            self._linux.ui.dogtail.rawinput.keyCombo('<Ctrl>h')

    def CloseVnc(self):
        log.info('Closing VNC')
        self._linux.ui.dogtail.procedural.run('pkill xsrvnc.bin')
        
    def CloseVncByKey(self):
        log.info('Closing VNC by Ctrl+H')
        if self.isVNCOpen():
            self._linux.ui.dogtail.rawinput.keyCombo('<Ctrl>h')