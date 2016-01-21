import time
import os
from logbook import Logger
log = Logger("PhoneApp")

class PhoneApp(object):
    def __init__(self, linux): 
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail

    def start(self):
        self._dogtail.rawinput.keyCombo('<Ctrl>H')

    def close(self):
        self._dogtail.rawinput.keyCombo('<Ctrl>H')

    def screenshot(self):
        self._dogtail.utils.screenshot('PhoneAppTestScreenshot.png', False)    

    @property
    def phoneapp(self):
        return self._driver

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    
    phoneapp = PhoneApp(sunriver.linux)
    phoneapp.start()
    phoneapp.close()




