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

    def start_chrome_android(self):
        androidUI = slash.g.sunriver.android.ui
        slash.g.sunriver.vnc.OpenVnc()
        slash.g.sunriver.desktop.openSpecificApp('Chrome')
        while not androidUI(resourceId="com.android.chrome:id/url_bar").exists:
            if androidUI(text="Accept & continue").exists:
                androidUI(text="Accept & continue").click()
                androidUI(text="No thanks").wait.exists
                androidUI(text="No thanks").click()
            if androidUI(text="Search or type URL").exists:
                androidUI(text="Search or type URL").click()
        androidUI(resourceId="com.android.chrome:id/url_bar").click()
        androidUI(resourceId="com.android.chrome:id/url_bar").set_text(self.video_url)
        androidUI.press('Enter')
        time.sleep(10)
        if androidUI(text='https://m.youtube.com/watch?v=YQHsXMglC9A').exists:
            slash.should.be(androidUI(text='https://m.youtube.com/watch?v=YQHsXMglC9A').exists, True)
        else:
            slash.should.be(androidUI(text='https://m.youtube.com').exists, True)

    def test_chromium(self):
        keycombo = slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo
        log.info("Testing Chrome on VNC")
        self.start_chrome_android()
        log.info("Testing Chromium")
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        time.sleep(5)
        keycombo('<Ctrl>c')
        slash.g.sunriver.vnc.CloseVnc()
        self.start_chrome()
        chromium = slash.g.chromium
        slash.should.be_in(self.first_url, chromium._driver.current_url)
        log.info('Chromium opened successfuly')
        keycombo('<Ctrl>l')
        keycombo('<Ctrl>a')
        keycombo('<BackSpace>')
        time.sleep(2)
        keycombo('<Menu>')
        time.sleep(2)
        for i in range(5): keycombo('<Down>'); time.sleep(1)
        keycombo('Enter')
        time.sleep(5)
        keycombo('Escape')
        slash.should.be_in(self.site_name, chromium._driver.current_url)
        chromium.skip_add()
        slash.g.sunriver.linux.ui.dogtail.utils.screenshot(file=self.screenshot_name, timeStamp=False)
        chromium.pause_video()
        chromium.play_video()
        chromium.youtube_fullscreen()
        keycombo('<Escape>')
        time.sleep(1)
        keycombo('<Ctrl>t')
        keycombo('<Ctrl>l')
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(self.second_url)
        keycombo('<Enter>')
        time.sleep(5)
        #slash.should.be_in(self.second_url_name, chromium._driver.current_url) selenium doesn't support tabs
        time.sleep(1)
        keycombo('<Ctrl>t')
        keycombo('<Ctrl>l')
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(self.third_url)
        keycombo('<Enter>')
        time.sleep(5)
        #slash.should.be_in(self.third_url_name, chromium._driver.current_url) selenium doesn't support tabs
        for i in range(4): time.sleep(2); chromium.switch_tab()
        chromium.stop()

    def test_libre(self):
        filename = str(datetime.now()).replace(':','-')
        self.start_libre_with_screenshot()
        slash.g.writer.write_text('inserting text')
        slash.g.writer.choose_slide()
        time.sleep(3)
        slash.g.writer.save_as(file_name=filename)
        slash.g.writer.stop()
