from email import message_from_string
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate, formataddr
from email import encoders

import time
from dateutil import parser
from bunch import Bunch

class LinuxMail(object):
    def __init__(self, linux):
        self._linux = linux
        self._imap_module = self._linux._rpyc.modules.imaplib
        self._smtp_module = self._linux._rpyc.modules.smtplib
        self._imap = self._imap_module.IMAP4("localhost")
        self._smtp = self._smtp_module.SMTP("localhost")
        self._key = self._read_key()

        self._email = None
        self._password = None
        self._folder = None
        self._count = None
    
    def _read_key(self):
        return self._linux.shell.shell("cat /run/imapsmtp/key").stdout.read().strip()

    def _assert_result(self, result):
        assert result == "OK"

    def _auth_string(self, email, password=""):
        return "\x00{} {}\x00{}".format(email, self._key, password)

    def choose_email(self, email, password=""):
        self._email = email
        self._password = password
        self._auth_token = self._auth_string(email, password)
        def authentication_callback(response):
            return self._auth_token
        result, _unused = self._imap.authenticate("PLAIN", authentication_callback)
        self._assert_result(result)
        result = self._smtp.docmd("AUTH PLAIN {}".format(self._auth_token.encode("base64")))
        assert "Logged in" == result[1]
        return self

    def is_logged_in(self):
        return self._imap.state != 'NONAUTH'

    def choose_folder(self, _folder):
        folder = { "inbox":  "INBOX"
                 , "drafts": "Drafts"
                 , "outbox": "Outbox"
                 , "sent":   "Sent"
                 , "trash":  "Trash"
                 }[_folder]
        self._folder = folder
        result, count = self._imap.select(folder)
        self._assert_result(result)
        self._count = int(count[0])
        return self

    def folders(self):
        result, _folders = self._imap.list()
        self._assert_result(result)
        folders = [x.split("/")[-1].replace('"', '').strip() for x in _folders]
        return folders

    def flags_string_to_bunch(self, flags_string):
        return Bunch(
            read    = ("\\Seen" in flags_string),
            starred = ("\\Flagged" in flags_string),
            deleted = ("\\Deleted" in flags_string),
            answered = ("\\Answered" in flags_string),
            attachment = False,
            favorite   = False,
            loaded     = False,
            )

    def load(self):
        result, data = self._imap.uid("fetch", "1:*", "(FLAGS)")
        self._assert_result(result)
        self._msgs = None
        if data[0] != None:
            _tmp = [x.split(" ", 3) for x in data]
            # dict indexed by uid
            self._flags = {int(x[2]): self.flags_string_to_bunch(x[3]) for x in _tmp}

            # for now, fetch all TODO: think about it
            uids_text = ','.join(map(str, self._flags.keys())) 
            result, data = self._imap.uid("fetch", uids_text, "(UID BODY[])") #)BODY.PEEK[HEADER.FIELDS (From To Cc Bcc Subject Date Message-ID Priority X-Priority References Newsgroups In-Reply-To Content-Type Reply-To)]")
            self._assert_result(result)
            # dict indexed by uid
            self._msgs = {int(x[0].split(" ", 3)[2]): message_from_string(x[1]) for x in data[::2]}
        return self
        #return data

    def messages(self):
        if self._msgs == None:
            return []
        _messages = [Bunch(
            _uid  = uid,
            time  = parser.parse(mail["date"]),
            from_ = '' if mail["from"] == None else mail["from"],
            to    = '' if mail["to"] == None else mail["to"],
            cc    = '' if mail["cc"] == None else mail["cc"],
            subject = mail["subject"],
            flags = self._flags[uid],
            body = Bunch(
                text = mail.get_payload()[0].get_payload(),
                html = mail.get_payload()[0].get_payload().decode('base64'),
                ),
            )
            for (uid, mail) in sorted(self._msgs.iteritems())]
        return _messages

    def send(self, to, subject, attachments = []):
        msg = MIMEMultipart()
        from_ = self._email
        msg['From'] = from_
        msg['To'] = to #COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime = True)
        self._smtp.sendmail( from_addr=msg['From']
                           , to_addrs=msg['To']
                           , msg=msg.as_string()
                           )

if __name__ == "__main__":
    import sys
    email = sys.argv[1]
    
    from sr_automation.utils.TimeIt import TimeIt
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    from sr_automation.platform.sunriver.applications.IMAPApp.IMAPApp import IMAPApp
    sunriver = Sunriver()
    sunriver.desktop.start()
    imap = IMAPApp(sunriver)
    imap.start()

    mail = LinuxMail(sunriver.linux)
    t = TimeIt()
    with t.measure():
        mail.choose_email(email).choose_folder("inbox").load()
    print t.measured

    import IPython
    IPython.embed()

    imap.stop()
    sunriver.desktop.stop()

