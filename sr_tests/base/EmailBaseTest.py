from logbook import Logger
import datetime
import os
import slash
from bunch import Bunch
import time
from email.header import decode_header

from BaseTest import BaseTest
from sr_automation.applications.AndroidMail import AndroidMail
from sr_automation.applications.IMAPApp import IMAPApp 

class EmailBaseTest(BaseTest):

    @slash.hooks.session_start.register
    def start_mail_sync():
        def _start_imapapp():
            #if slash.g.device.linux.shell.is_running_by_short_name("imapapp"):
            #    return
            username = "labuser"
            filesystem_fix_after_boot = " ; ".join([
                "USER={}".format(username)
                , "mkdir /tmp_imap 2>/dev/null"
                , "chmod 755 /tmp_imap"
                , "mount -t tmpfs none /tmp_imap"
                , "chmod 755 /tmp_imap"
                , "stat /bin/imapsmtp.bak 2>/dev/null || cp -n /bin/imapsmtp /bin/imapsmtp.bak"
                , "rm /tmp_imap/imapsmtp -rf"
                , "cp /bin/imapsmtp.bak /tmp_imap/imapsmtp"
                , "chown root:$USER /tmp_imap/imapsmtp"
                , "setcap CAP_NET_BIND_SERVICE+ep /tmp_imap/imapsmtp"
                , "chmod 110 /tmp_imap/imapsmtp"
                , "ln -sf /tmp_imap/imapsmtp /bin/imapsmtp"
                , "chown -h root:$USER /bin/imapsmtp"])
            slash.g.device.linux.shell.shell(filesystem_fix_after_boot).wait()
            slash.g.device.linux.shell.shell('su - {} -c "/home/labuser/imap_config.py &"'.format(username))
            while not slash.g.device.linux.shell.is_running_by_short_name("imap_config.py"): pass
            IMAPAPP_TITLE = "ImapApp"
            slash.g.device.android.cmd("shell am start -n com.example.imapapp/.TestActivity")
            time.sleep(2)
            slash.g.device.android.ui(text = IMAPAPP_TITLE).wait.exists()
            if not slash.g.device.android.ui.press.home(): # try again
                time.sleep(0.5)
                slash.g.device.android.ui.press.home()
            while slash.g.device.linux.shell.is_running_by_short_name("imap_config.py"): pass
            return True

        #_start_imapapp()
        slash.g.mail = Bunch(
            android = AndroidMail(slash.g.device.android),
            linux   = IMAPApp(slash.g.device.linux),
            email   = None,
            password = None,
            folder  = None,
            )
        slash.g.messages = Bunch(
            android = None,
            linux   = None,
            )

    @slash.hooks.session_end.register
    def stop_mail_sync():
        def _kill_imapapp():
            slash.g.device.android.cmd("shell am force-stop com.example.imapapp")
            slash.g.device.linux.shell.shell("killall -9 imapsmtp")
        _kill_imapapp()

    @property
    def mail(self):
        return slash.g.mail

    @property
    def messages(self):
        return slash.g.messages

    def before(self):
        super(EmailBaseTest, self).before()
        if self.mail.linux._imap.state == 'NONAUTH':
            self.choose_email("srusertest@gmail.com")

    def after(self):
        super(EmailBaseTest, self).after()

    def _folder_mapper(self, name):
        name = name.lower()
        return {"inbox":  Bunch(linux = "INBOX", android = "Inbox"),
                "drafts": Bunch(linux = "Drafts", android = "Drafts"),
                "outbox": Bunch(linux = "Outbox", android = "Outbox"),
                "sent":   Bunch(linux = "Sent", android = "Sent"),
                "trash":  Bunch(linux = "Trash", android = "Trash"),
                }[name]

    def choose_email(self, email, password=None):
        self.mail.email = email
        self.mail.password = password
        self.mail.android.choose_email(email, password)
        self.mail.linux.choose_email(email, password)
        return self

    def choose_folder(self, _folder):
        folder = self._folder_mapper(_folder)
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
                if a.from_ != l.from_]

    def compare_to(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a.to != l.to]

    def compare_cc(self):
        return [i for (i, (a, l)) in enumerate(zip(self.messages.android, self.messages.linux))
                if a.cc != l.cc]
    
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
            if (a_body.text is not None) and (l_body.text is not None):
                if (len(a_body.text) > 0) and (len(l_body.text) > 0):
                    if a_msg.body.text.encode('utf8') != l_msg.body.text.decode('base64'):
                        different.append(index)
                        continue
            if (a_body.html is not None) and (l_body.html is not None):
                if (len(a_body.html) > 0) and (len(l_body.html) > 0):
                    if a_msg.body.html.encode('utf8') != l_msg.body.html:
                        different.append(index)
        return different

    def compare_attachments(self):
        return [] # False

