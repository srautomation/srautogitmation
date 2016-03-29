import time
import os
from logbook import Logger
log = Logger("Browser")

class Chromium(object):
    def __init__(self, linux): 
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail
        self._webdriver = self._linux.ui.webdriver

    def start(self):
        log.warn('Starting Chromium')
        self._driver = self._webdriver.Chrome(os.path.expanduser('/usr/lib/chromium/chromedriver'))
        time.sleep(4) # Chrome needs time to open

    def stop(self):
        self._linux.cmd('pkill chromium')

    @property
    def chromium(self):
        return self._driver

    def youtube_settings(self):
        self._driver.find_element_by_id('settings_button').click()
        time.sleep(4)

    def open_youtube_video(self, videoURL):
        self._driver.get("http://www.youtube.com/%s"%videoURL)

    def open_url(self, url):
        self._driver.get(url)
        time.sleep(5)

    def play_video(self):
        self._driver.execute_script('document.getElementsByTagName("video")[0].play()')
        time.sleep(5)

    def pause_video(self):
        self._driver.execute_script('document.getElementsByTagName("video")[0].pause()')
        time.sleep(5)

    def youtube_fullscreen(self):
        self._driver.find_element_by_class_name('ytp-fullscreen-button').click()
        time.sleep(8)#show a little bigscreen

    def skip_add(self, counter=0):
        try:
            counter+=1
            if counter < 7:
                if self._driver.find_element_by_class_name('videoAdUiSkipButton'):
                    log.info('Skipping Add')
                    self._driver.find_element_by_class_name('videoAdUiSkipButton').click()
        except:
            log.info('Unable to find Skip Add trying again')
            self.skip_add(counter)

    def escape(self):
        self._webdriver.common.keys.Keys.ESCAPE    
 
    def new_tab(self, window='_blank'):
        self._driver.execute_script("window.open(%s);"%window)
        time.sleep(16) # let the tab time to open

    def switch_tab(self):
        self._dogtail.rawinput.keyCombo('<Ctrl>PageUp')
        time.sleep(5)

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    
    browser = Chromium(sunriver.linux)
    browser.start()
    browser._driver.execute_script("window.open('http://www.cnn.com');")
