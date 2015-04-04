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

@slash.hooks.result_summary.register
def stop_mail_sync():
    log.info("Stopping IMAPApp")
    slash.g.imapapp.stop()
    slash.g.mail = None


class MailBaseTest(BaseTest):
    def before(self):
        super(MailBaseTest, self).before()
        self.mail = slash.g.mail
        self.messages = slash.g.messages
   #     if self.mail.linux._imap.state == 'NONAUTH':
   #         self.choose_email("srusertest@gmail.com")
    
    def test(self):
        import IPython
        IPython.embed()

    def choose_email(self, email, password=None):
        self.mail.email = email
        self.mail.password = password
        self.mail.android.choose_email(email, password)
        self.mail.linux.choose_email(email, password)
        return self

    def choose_folder(self, _folder):
        self.mail.folder = folder
        self.mail.android.choose_folder(self.mail.folder.android)
        self.mail.linux.choose_folder(self.mail.folder.linux)
        return self

    def load(self):
        self.mail.android.load()
        self.mail.linux.load()
        self.messages.android = self.mail.android.messages()
        self.messages.linux   = self.mail.linux.messages()

    def compare_all(self):
        return (self.compare_count()             and 
                not bool(self.compare_from())    and 
                not bool(self.compare_to())      and
                not bool(self.compare_cc())      and
                not bool(self.compare_subject()) and
                not bool(self.compare_flags())   and
                not bool(self.compare_body()))

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
    
    def compare_subject(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a.subject.encode('utf8') != decode_header(l.subject)[0][0].replace("\r\n", "")]

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
