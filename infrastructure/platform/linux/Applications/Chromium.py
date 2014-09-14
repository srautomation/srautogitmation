import Application

class Chromium(Application._Application):
    def __init__(self, cmd, ui):
        super(Chromium, self).__init__(cmd, ui, 'su -c "chromium-browser %s" labuser', '*chromium')
            
    def start(self, url):
        self._app_cmd = self._app_cmd % url
        super(Chromium, self).start()

    def stop(self):
        self._cmd('pkill -9 chrom')
