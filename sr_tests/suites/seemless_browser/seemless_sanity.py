from logbook import Logger
log = Logger("Sanity Seemless operation")
import time
import slash
from sr_tests.suites.seemless_browser.Base import SeemlessBrowserTest

class SeemlessSanity(SeemlessBrowserTest):
    
    slash.g.counter = 0

    def before(self):
        super(SeemlessSanity, self).before()

    def start_chrome_android(self):
        slash.g.sunriver.vnc.OpenVnc()
        slash.g.sunriver.desktop.openSpecificApp('Chrome')
        while not slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").exists:
            if slash.g.sunriver.android.ui(text="Accept & continue").exists:
                slash.g.sunriver.android.ui(text="Accept & continue").click()
                slash.g.sunriver.android.ui(text="No thanks").wait.exists
                slash.g.sunriver.android.ui(text="No thanks").click()
            if slash.g.sunriver.android.ui(text="Search or type URL").exists:
                slash.g.sunriver.android.ui(text="Search or type URL").click()
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").set_text('www.youtube.com/watch?v=YQHsXMglC9A')
        slash.g.sunriver.android.ui.press('Enter')


    def test_chromium(self):
        self.start_chrome_android()
        log.info("Testing Chromium")
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        time.sleep(5)
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>c')
        self.start_chrome()
        #slash.g.chromium.open_youtube_video("watch?v=YQHsXMglC9A")
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>l')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>a')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<BackSpace>')
        time.sleep(2)
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Menu>')
        time.sleep(2)
        for i in range(5):
            slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Down>')
            time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('Enter')
        log.info('pasted video')
        time.sleep(25) # allow video loading
        slash.g.chromium.skip_add()
        slash.g.sunriver.linux.ui.dogtail.utils.screenshot(file='chromeShot.png', timeStamp=False)
        slash.g.chromium.pause_video()
        slash.g.chromium.play_video()
        slash.g.chromium.youtube_fullscreen()
        slash.g.chromium.escape()
        slash.g.chromium._driver.execute_script("window.open('http://www.cnn.com');")
        time.sleep(12) # let the website upload
        slash.g.chromium._driver.execute_script("window.open('http://www.nba.com');")
        time.sleep(12) # let the website upload
        for i in range(4):
            time.sleep(2)
            slash.g.chromium.switch_tab()
        slash.g.chromium.stop()

    def test_libre(self):
        self.start_libre_with_screenshot()
        slash.g.writer.write_text('inserting text')
        slash.g.writer.choose_slide()
        time.sleep(3)#wait for save button to appear
        slash.g.writer.save_as(file_name='file')       
