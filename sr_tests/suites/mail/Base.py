from sr_automation.platform.android.applications.Mail.Mail import AndroidMail
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
from sr_automation.platform.linux.applications.Mail.Mail import LinuxMail
from sr_automation.platform.sunriver.applications.IMAPApp.IMAPApp import IMAPApp
from sr_tests.base.Base import BaseTest

from email.header import decode_header
from bunch import Bunch
import slash

from logbook import Logger
log = Logger("MailBaseTest")

@slash.hooks.session_start.register
def start_mail_sync():
    log.info("Starting IMAPApp")
    slash.g.imapapp = IMAPApp(slash.g.sunriver)
    slash.g.imapapp.start()

    slash.g.mail = Bunch( android  = AndroidMail(slash.g.sunriver.android)
                        , linux    = LinuxMail(slash.g.sunriver.linux)
                        , email    = None
                        , password = None
                        , folder   = None
                        )
    slash.g.messages = Bunch( android = None
                            , linux   = None
                            )

@slash.hooks.session_end.register
def stop_mail_sync():
    log.info("Stopping IMAPApp")
    slash.g.imapapp.stop()
    slash.g.mail = None


class MailBaseTest(BaseTest):

    def before(self):
        super(MailBaseTest, self).before()
        if not self.mail.linux.is_logged_in():
            self.choose_email(slash.config.sr.mail.sender)


    def choose_email(self, email, password=None):
        self.mail.email = email
        self.mail.password = password
        self.mail.android.choose_email(email, password)
        self.mail.linux.choose_email(email, password)
        return self

    def choose_folder(self, _folder):
        self.mail.folder = _folder
        self.mail.android.choose_folder(self.mail.folder)
        self.mail.linux.choose_folder(self.mail.folder)
        return self

    def load(self):
        self.mail.android.load()
        self.mail.linux.load()
        self.messages.android = self.mail.android.messages()
        self.messages.linux   = self.mail.linux.messages()

    def compare_all(self):
        slash.should.be(self.compare_count(), True)
        slash.should.be(len(self.compare_from()), 0)
        slash.should.be(len(self.compare_to()), 0)
        slash.should.be(len(self.compare_cc()), 0)
        slash.should.be(len(self.compare_subject()), 0)
        slash.should.be(len(self.compare_body()), 0)
        #slash.should.be(len(self.compare_flags()), True)

    def compare_count(self):
        return len(self.messages.android) == len(self.messages.linux)

    def compare_uid(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a._uid != l._uid]

    def compare_from(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if self.clean_addresses(a.from_) != self.clean_addresses(l.from_)]

    def compare_to(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if self.clean_addresses(a.to) != self.clean_addresses(l.to)]

    def compare_cc(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if self.clean_addresses(a.cc) != self.clean_addresses(l.cc)]

    def clean_addresses(self, addresses):
        if addresses == None:
            return ''
        addresses = addresses.replace(' ','').split(',')
        addresses = map(self.clean_address, addresses)
        return addresses

    def clean_address(self, address):
        tag_index = address.find('<')
        if tag_index != -1:
            address = address[tag_index + 1:address.find('>')]
        return address.encode('utf8')

    def clean_subject(self, subject):
        if subject == None:
            return ''
        return subject
    
    def compare_subject(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a.subject.encode('utf8') != decode_header(self.clean_subject(l.subject))[0][0].replace("\r\n", "")]

    def compare_date(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a.time != l.time]

    def compare_flags(self):
        return [] # False

    def compare_body(self):
        different = []
        for index, (a_msg, l_msg) in enumerate(zip(self.messages.android, self.messages.linux)):
            a_body = a_msg.body
            l_body = l_msg.body
            html_not_equal = False
            text_not_equal = False
            if (a_body.text is not None) and (l_body.text is not None):
                if (len(a_body.text) > 0) and (len(l_body.text) > 0):
                    if a_msg.body.text.encode('utf8') != l_msg.body.text.decode('base64'):
                        text_not_equal = True
            if (a_body.html is not None) and (l_body.html is not None):
                if (len(a_body.html) > 0) and (len(l_body.html) > 0):
                    if a_msg.body.html.encode('utf8') != l_msg.body.html:
                        html_not_equal = True
            if text_not_equal and html_not_equal:
                different.append(index)
        return different

    def compare_attachments(self):
        return [] # False

    @property
    def mail(self):
        return slash.g.mail

    @property
    def messages(self):
        return slash.g.messages
