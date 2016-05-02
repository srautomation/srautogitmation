from logbook import Logger
log = Logger("Sanity Seamless operation")
import time
import slash
from sr_tests.suites.seamless_browser.Base import SeamlessBrowserTest
from datetime import datetime

class SeamlessSanity(SeamlessBrowserTest):
    
    video_url = 'https://www.youtube.com/watch?v=YQHsXMglC9A'
    first_url = 'data:,'
    second_url = 'http://www.cnn.com'
    second_url_name = 'cnn'
    third_url = 'http://www.nba.com'
    third_url_name = 'nba'
    site_name = 'youtube'
    screenshot_name = 'chromeShot.png'
    
    def before(self):
        super(SeamlessSanity, self).before()

    def test_chromium(self):
        keycombo = slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo
        log.info("Testing Chrome on VNC")
        self.sunriver.vnc.OpenVnc()
        self.goto_youtube_in_android_chrome("https://m.youtube.com/watch?v=YQHsXMglC9A")
        log.info("Testing Chromium")
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        time.sleep(5)
        keycombo('<Ctrl>c')
        slash.g.sunriver.vnc.CloseVnc()
        self.start_chromium()
        chromium = slash.g.chromium
        log.info('Pasting link from android chrome')
        keycombo('<Ctrl>l')
        keycombo('<Ctrl>a')
        keycombo('<Ctrl>v')
        keycombo('<Enter>')
        time.sleep(5)
        log.info('Opening tab with '+self.second_url)
        keycombo('<Ctrl>t')
        keycombo('<Ctrl>l')
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(self.second_url)
        keycombo('<Enter>')
        time.sleep(5)
        log.info('Opening tab with '+self.third_url)
        keycombo('<Ctrl>t')
        keycombo('<Ctrl>l')
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(self.third_url)
        keycombo('<Enter>')
        time.sleep(3)
        for i in range(4): time.sleep(2); chromium.switch_tab()
        chromium.stop()

    def test_libre(self):
        slash.g.sunriver.linux.ui.dogtail.utils.screenshot(file=self.screenshot_name, timeStamp=False)
        filename = str(datetime.now()).replace(':','-')
        try:
            self.start_libre_with_screenshot()
            slash.g.writer.write_text('inserting text')
            slash.g.writer.choose_slide()
            time.sleep(3)
            slash.g.writer.save_as(file_name=filename)
            slash.g.writer.stop()
        except SystemExit:
            slash.should.be_true(False)
