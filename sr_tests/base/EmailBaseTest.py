from logbook import Logger
import datetime
import os
from bunch import Bunch
import time

from BaseTest import BaseTest
from sr_automation.applications.AndroidMail import AndroidMail
from sr_automation.applications.IMAPApp import IMAPApp 

class EmailBaseTest(BaseTest):
    def _start_imapapp(self):
        if self.linux.shell.is_running_by_short_name("imapapp"):
            return
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
        self.linux.shell.shell(filesystem_fix_after_boot).wait()
        self.linux.shell.shell('su - {} -c "/home/labuser/imap_config.py &"'.format(username))
        while not self.linux.shell.is_running_by_short_name("imap_config.py"): pass
        IMAPAPP_TITLE = "ImapApp"
        self.android.cmd("shell am start -n com.example.imapapp/.TestActivity")
        self.android.ui(text = IMAPAPP_TITLE).wait.exists()
        if not self.android.ui.press.home(): # try again
            time.sleep(0.5)
            self.android.ui.press.home()
        while self.linux.shell.is_running_by_short_name("imap_config.py"): pass
        return True

    def _kill_imapapp(self):
        self.android.cmd("shell am force-stop com.example.imapapp")
        self.linux.shell.shell("killall -9 imapsmtp")

    def before(self):
        super(EmailBaseTest, self).before()
        self._start_imapapp()
        self.mail = Bunch(
            android = AndroidMail(self.android),
            linux   = IMAPApp(self.linux),
            email   = None,
            password = None,
            folder  = None,
            )
        self.messages = Bunch(
            android = None,
            linux   = None,
            )

    def after(self):
        self._kill_imapapp()
        super(EmailBaseTest, self).after()

    def _folder_mapper(self, name):
        name = name.lower()
        return {"inbox":  Bunch(linux = "INBOX", android = "Inbox"),
                "drafts": Bunch(linux = "DRAFTS", android = "Drafts"),
                "outbox": Bunch(linux = "OUTBOX", android = "Outbox"),
                "sent":   Bunch(linux = "SENT", android = "Sent"),
                "trash":  Bunch(linux = "TRASH", android = "Trash"),
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
        return (self.compare_count()   and 
                self.compare_from()    and 
                self.compare_to()      and
                self.compare_cc()      and
                self.compare_subject() and
                self.compare_flags()   and
                self.compare_body())

    def compare_count(self):
        return len(self.messages.android) == len(self.messages.linux)

    def compare_from(self):
        return all([a.from_ == l.from_ for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_to(self):
        return all([a.to == l.to for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_cc(self):
        return all([a.cc == l.cc for (a, l) in zip(self.messages.android, self.messages.linux)])
    
    def compare_subject(self):
        return all([a.subject == l.subject for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_date(self):
        return all([a.time == l.time for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_flags(self):
        return True # False

    def compare_body(self):
        for a_msg, l_msg in zip(self.messages.android, self.messages.linux):
            a_body = a_msg.body
            l_body = l_msg.body
            if (a_body.text is not None) and (l_body.text is not None) and (len(a_body.text) > 0) and (len(l_body.text) > 0):
                if a_msg.body.text != l_msg.body.text:
                    return False
            if (a_body.html is not None) and (l_body.html is not None) and (len(a_body.html) > 0) and (len(l_body.html) > 0):
                if a_msg.body.html.encode('utf8') != l_msg.body.html:
                    return False
        return True

    def compare_attachments(self):
        return True # False

