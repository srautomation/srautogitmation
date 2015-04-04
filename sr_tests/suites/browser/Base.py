from sr_tests.base.BaseTest import BaseTest
from sr_automation.applications import Browser

class BrowserBaseTest(BaseTest):
    def init_chromium(self):
        self.browser = Browser.Browser(self.linux)
        self.browser.start()
        return self.browser.chromium
