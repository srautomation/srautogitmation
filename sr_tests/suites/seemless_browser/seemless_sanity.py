from logbook import Logger
log = Logger("Sanity Seemless operation")
import time
import slash
from sr_tests.suites.seemless_browser.Base import SeemlessBrowserTest

class SeemlessSanity(SeemlessBrowserTest):
    
    video_url = 'https://www.youtube.com/watch?v=YQHsXMglC9A'
    appName = 'Chrome'
    first_url = 'data:,'
    second_url = 'http://www.cnn.com'
    second_url_name = 'cnn'
    third_url = 'http://www.nba.com'
    third_url_name = 'nba'
    android_chrome_url = 'https://m.youtube.com/watch?v=YQHsXMglC9A'
    site_name = 'youtube'
    screenshot_name = 'chromeShot.png'
    
    def before(self):
        super(SeemlessSanity, self).before()

    def start_chrome_android(self):
        androidUI = slash.g.sunriver.android.ui
        slash.g.sunriver.vnc.OpenVnc()
        slash.g.sunriver.desktop.openSpecificApp(self.appName)
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
        time.sleep(4)
        self.compare_chrome_android(self.android_chrome_url)

    def test_chromium(self):
        keycombo = slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo
        self.start_chrome_android()
        log.info("Testing Chromium")
        slash.g.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        time.sleep(5)
        keycombo('<Ctrl>c')
        self.start_chrome()
        chromium = slash.g.chromium
        self.compare_url(self.first_url, chromium._driver.current_url)#checks if chrome has loaded
        #slash.g.chromium.open_youtube_video("watch?v=YQHsXMglC9A")
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
        self.compare_url(self.site_name, chromium._driver.current_url)#checks if url is copied successfully from phone
        chromium.skip_add()
        slash.g.sunriver.linux.ui.dogtail.utils.screenshot(file=self.screenshot_name, timeStamp=False)
        chromium.pause_video()
        chromium.play_video()
        chromium.youtube_fullscreen()
        chromium.escape()
        chromium.new_tab(self.second_url)#opens cnn url
        self.compare_url(self.second_url_name, chromium._driver.current_url)
        chromium.new_tab(self.third_url)#opens nba url
        self.compare_url(self.third_url_name, chromium._driver.current_url)
        for i in range(4): time.sleep(2); chromium.switch_tab()
        chromium.stop()

    def test_libre(self):
        self.start_libre_with_screenshot()
        slash.g.writer.write_text('inserting text')
        slash.g.writer.choose_slide()
        time.sleep(3)#wait for save button to appear
        slash.g.writer.save_as(file_name='file')       
