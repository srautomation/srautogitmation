from BaseSendTests import BaseSendTests
from sr_automation.platform.linux.applications.Mail.GUI import LinuxMailGUI
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import time


class SanityMailTest(BaseSendTests):

    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def start_linux_gui():
        slash.g.mail.linuxGUI = LinuxMailGUI(slash.g.sunriver.linux)

    def before(self):
        super(SanityMailTest, self).before()



    def after(self):
        super(SanityMailTestTests, self).before()
        time.sleep(2)
