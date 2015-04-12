from selenium import webdriver
import time

from logbook import Logger
log = Logger("Browser")

class Browser(object):
    CHROMEDRIVER_RPC_PORT = 12356
    def __init__(self, linux): 
        self._linux = linux
        self._open_tabs = 0

    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("/usr/local/CHROMEDRIVER --port={} --whitelisted-ips *".format(Browser.CHROMEDRIVER_RPC_PORT))
        time.sleep(4) # TODO: change this hack
        self._driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.CHROME, 
                                        command_executor="http://%s:%d" % (self._linux.ip, Browser.CHROMEDRIVER_RPC_PORT)
                                        )
        log.info("RemoteDriver Connected")
        self._open_tabs += 1
        self._title = 'Chromium' # used by _Application.grab_focus()

    def stop(self):
        if self._driver is not None:
            try:
                self._driver.close()
            except Exception, e: # TODO: fix hack
                log.info(e)

    @property
    def chromium(self):
        return self._driver
   
    # TODO: change self.*_tab() to be self._driver.*_tab()
    def new_tab(self):
        self._dogtail.rawinput.keyCombo('<Ctrl>T')
        time.sleep(5) # let the tab time to open
        self._driver.switch_to.window(self._driver.window_handles[self._open_tabs])
        self._open_tabs += 1

    def switch_tab(self, num):
        " num is the tabs number, starting from 1 "
        if num <= self._open_tabs:
            self._dogtail.rawinput.keyCombo('<Alt>{}'.format(num))
            self._driver.switch_to.window(self._driver.window_handles[num - 1])
        else:
            raise ValueError('There are only {} tabs open'.format(self._open_tabs))

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    browser = Browser(sunriver.linux)
    browser.start()
    import IPython
    IPython.embed()
    browser.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()



