import Application

class Chromium(Application._Application):
    def __init__(self, linux):
        super(Chromium, self).__init__(linux, 'su -c "chromium-browser %s" labuser', 'pkill -9 chrom')
            
    def start(self, url):
        self._start_cmd = self._start_cmd % url
        super(Chromium, self).start()
