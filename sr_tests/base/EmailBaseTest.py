import time

from BaseTest import BaseTest

class EmailBaseTest(BaseTest):
    def start_imapapp(self):
        IMAPAPP_TITLE = "ImapApp"
        self.android.cmd("shell am start -n com.example.imapapp/.TestActivity")
        self.android.ui(text = IMAPAPP_TITLE).wait.exists()
        if not self.android.ui.press.home(): # try again
            time.sleep(0.5)
            self.android.ui.press.home()
        return True
