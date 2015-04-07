from BaseSendTests import BaseSendTests
from sr_automation.platform.linux.applications.Mail.GUI import LinuxMailGUI
import slash
import slash.log
import IPython

class LinuxEmailSendTests(BaseSendTests):

    @slash.hooks.session_start.register
    def start_linux_gui():
        slash.g.mail.linuxGUI = LinuxMailGUI(slash.g.sunriver.linux)

    def send_mail(self, to, subject, body, attachments = []):
        #slash.g.mail.linuxGUI.send(to,subject,body,attachments)
        slash.g.mail.linux.send(to, subject, body, attachments)
        #sentSuccessfully = self.mail.linux.send(to, subject, body, attachments)
        #slash.should.be(sentSuccessfully, True)
