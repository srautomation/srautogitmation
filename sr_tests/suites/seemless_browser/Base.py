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
        log.info("Starting LibreOffice")
        slash.g.writer = Writer(slash.g.sunriver.linux)
        slash.g.writer.start(option='/tmp/dogtail-BigScreen/chromeShot.png')

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)

    def compare_url(self, urlA, urlB):
        if urlA in urlB:
            log.info('correct')
        else:
            log.info('not the expected url')
        
    def compare_chrome_android(self, url):
        if slash.g.sunriver.android.ui(text=url).exists:
            assert 1 == 1 #needs to be changed to something realistic
        else:
            slash.add_error('The URLS are not the same')
        
