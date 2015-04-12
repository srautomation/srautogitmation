from Base import MailBaseTest
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import slash.log
import IPython
import time

class StarredTests(MailBaseTest):


    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def after(self):
        self.load()
        self.compare_all()
        super(StarredTests, self).after()

    def before(self):
        super(StarredTests, self).before()
        self.choose_folder('inbox')

    def test_star_in_android(self):
        if slash.g.sunriver.desktop.is_desktop_running():
            slash.g.sunriver.switch_to_android.switch()
        slash.g.mail.androidGUI.choose_folder('inbox')
        slash.g.mail.androidGUI.add_star()

    def test_unstar_in_android(self):
        if slash.g.sunriver.desktop.is_desktop_running():
            slash.g.sunriver.switch_to_android.switch()
        slash.g.mail.androidGUI.choose_folder('inbox')
        slash.g.mail.androidGUI.remove_star()

   # def test_star_in_linux(self):
   #     pass

   # def test_unstar_in_linux(self):
   #     pass

