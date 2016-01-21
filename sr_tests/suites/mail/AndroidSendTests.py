from BaseSendTests import BaseSendTests
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import slash.log
import IPython

class AndroidSendTests(BaseSendTests):

    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def before(self):
        super(AndroidSendTests, self).before()
        slash.g.sunriver.switch_to_android.switch()

    def after(self):
        super(AndroidSendTests, self).before()

    def send_mail(self, to, subject, body, attachments = []):
        #self.choose_email('srusertest@gmail.com')
        slash.g.mail.androidGUI.send(to, subject, body, attachments)
        #slash.should.be(sentSuccessfully, True)
