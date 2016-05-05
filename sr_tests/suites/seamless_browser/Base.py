from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Browser.Browser import Chromium
from sr_automation.platform.linux.applications.Libreoffice.Writer import Writer
import time
import os
from logbook import Logger
log = Logger("Seamless Operation and Browser")

class SeamlessBrowserTest(BaseTest):

    def before(self):
        super(SeamlessBrowserTest, self).before()

    def start_chromium(self):
        slash.g.chromium = Chromium(slash.g.sunriver.linux)
        slash.g.chromium.start()

    def start_libre_with_screenshot(self):    
        log.info("Starting LibreOffice")
        slash.g.writer = Writer(slash.g.sunriver.linux)
        slash.g.writer.start(option='/tmp/dogtail-BigScreen/chromeShot.png')
    
    def pass_android_chrome_initial_screens(self):
        while not self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").exists:
            if self.sunriver.android.ui(text="Accept & continue").exists:
                self.sunriver.android.ui(text="Accept & continue").click()
                self.sunriver.android.ui(text="No thanks").wait.exists
                self.sunriver.android.ui(text="No thanks").click()
            if self.sunriver.android.ui(text="Search or type URL").exists:
                self.sunriver.android.ui(text="Search or type URL").click()
    
    def goto_youtube_in_android_chrome(self, i_videoLink):
        self.sunriver.desktop.openSpecificApp('Chrome')
        self.pass_android_chrome_initial_screens()
        if self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").exists:
            self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
            self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").set_text(i_videoLink)
        else:
            assert self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").exists == True , "Unable to pass initial screens in android chrome"
        self.sunriver.android.ui.press('Enter')
        time.sleep(10)
        if not self.sunriver.android.ui(text=i_videoLink).exists:
            assert self.sunriver.android.ui(text='https://m.youtube.com').exists == True , "Unable to open link in android chrome"
            
    def search_image_in_android_chrome(self, i_valueToSearch):
        self.sunriver.desktop.openSpecificApp('Chrome')
        self.pass_android_chrome_initial_screens()
        self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").click()
        self.sunriver.android.ui(resourceId="com.android.chrome:id/url_bar").set_text("https://images.google.com")
        self.sunriver.android.ui.press('Enter')
        self.sunriver.android.ui(description="Search").click()
        os.system("adb shell input text "+i_valueToSearch)
        self.sunriver.android.ui(description="Google Search").click()