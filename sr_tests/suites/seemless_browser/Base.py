from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Browser.Browser import Chromium
from sr_automation.platform.linux.applications.Libreoffice.Writer import Writer
import time
from logbook import Logger
log = Logger("Seemless Operation and Browser")

class SeemlessBrowserTest(BaseTest):

    def before(self):
        super(SeemlessBrowserTest, self).before()

    def start_chrome(self):
        slash.g.chromium = Chromium(slash.g.sunriver.linux)
        slash.g.chromium.start()

    def start_libre_with_screenshot(self):    
        log.warn("Starting LibreOffice")
        slash.g.writer = Writer(slash.g.sunriver.linux)
        slash.g.writer.start(option='/tmp/dogtail-BigScreen/chromeShot.png')

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
