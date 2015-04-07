from BaseSendTests import BaseSendTests
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import slash.log
import IPython

class AndroidSendTests(BaseSendTests):

    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def send_mail(self, to, subject, body, attachments = []):
        #self.choose_email('srusertest@gmail.com')
        if slash.g.sunriver.desktop.is_desktop_running():
            slash.g.sunriver.switch_to_android.switch()
        slash.g.mail.androidGUI.send(to, subject, body, attachments)
        if body == "":
            self.android.ui(text='Send').click()
        #slash.should.be(sentSuccessfully, True)
