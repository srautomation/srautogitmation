from tests.base.BaseTest import BaseTest
from infrastructure.applications import Browser

class BrowserBaseTest(BaseTest):
    def init_chromium(self):
        self.browser = Browser.Browser(self.linux)
        self.browser.start()
        return self.browser.chromium
