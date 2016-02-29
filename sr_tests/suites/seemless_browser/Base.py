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
        slash.g.writer.start(option='/tmp/dogtail-BigScreen/screen.png')
    
    def test_chromium(self):
        self.start_chrome()
        log.info("Testing Chromium")
        slash.g.chromium.open_youtube_video("watch?v=YQHsXMglC9A")
        time.sleep(15) # allow video loading
        slash.g.sunriver.linux.ui.dogtail.utils.screenshot(file='chromeShot.png', timeStamp=False)
        slash.g.chromium.pause_video()
        time.sleep(5)
        slash.g.chromium.play_video()
        slash.g.chromium.youtube_fullscreen()
        time.sleep(5)
        slash.g.chromium.escape()
        slash.g.chromium._driver.execute_script("window.open('http://www.cnn.com');")
        time.sleep(6) # let the website upload
        slash.g.chromium._driver.execute_script("window.open('http://www.nba.com');")
        time.sleep(6) # let the website upload
        for i in range(4):
            slash.g.chromium.switch_tab()
        slash.g.chromium.stop()

    def test_libre(self):
        self.start_libre_with_screenshot()
        slash.g.writer.save_as(file_name='file')       

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
