from sr_tests.base.Base import BaseTest
from sr_automation.platform.linux.applications.Browser.Browser import Chromium

class BrowserBaseTest(BaseTest):
    def test_chromium(self):
        self.browser = Browser.Browser(self.linux)
        self.browser.start()
        return self.browser.chromium
