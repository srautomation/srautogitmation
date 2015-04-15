from sr_tests.suites.mail.BaseLoadTests import BaseLoadTests
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash

class AndroidLoadTests(BaseLoadTests):

    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def before(self):
        super(BaseLoadTests, self).before()
        if slash.g.sunriver.desktop.is_desktop_running():
            slash.g.sunriver.switch_to_android.switch()

    def send_mail(self, to, subject, body):
        slash.g.mail.androidGUI.send(to, subject, body)

    def delete_from_sent(self):
        slash.g.mail.androidGUI.choose_folder('sent')
        slash.g.mail.androidGUI.delete_message()
        
