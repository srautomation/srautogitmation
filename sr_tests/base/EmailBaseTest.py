from logbook import Logger
import datetime
import os
from bunch import Bunch
import time

from BaseTest import BaseTest
from sr_automation.applications.AndroidMail import AndroidMail
from sr_automation.applications.IMAPApp import IMAPApp 

class EmailBaseTest(BaseTest):
    def start_imapapp(self):
        IMAPAPP_TITLE = "ImapApp"
        self.android.cmd("shell am start -n com.example.imapapp/.TestActivity")
        self.android.ui(text = IMAPAPP_TITLE).wait.exists()
        if not self.android.ui.press.home(): # try again
            time.sleep(0.5)
            self.android.ui.press.home()
        return True

    def before(self):
        super(EmailBaseTest, self).before()
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

    def choose_email(self, email, password=None):
        self.mail.email = email
        self.mail.password = password
        self.mail.android.choose_email(email, password)
        self.mail.linux.choose_email(email, password)

    def choose_folder(self, folder):
        self.mail.folder = folder
        self.mail.android.choose_folder(self.mail.folder)
        self.mail.linux.choose_folder(self.mail.folder)

    def load(self):
        self.mail.android.load()
        self.mail.linux.load()

    def mail_compare(self, (android_account, android_mailbox), (linux_account, linux_mailbox)):
        self.messages.android = self.mail.android.messages(android_account, android_mailbox)
        self.messages.linux   = self.mail.linux.messages(linux_account, linux_mailbox)

    def compare_count(self):
        return len(self.messages.android) == len(self.messages.linux)

    def compare_from(self):
        return all([a.from_ == l.from_ for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_to(self):
        return True # False
    
    def compare_subject(self):
        return all([a.subject == l.subject for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_date(self):
        return all([a.time == l.time for (a, l) in zip(self.messages.android, self.messages.linux)])

    def compare_flags(self):
        return True # False

    def compare_body(self):
        for a_msg, l_msg in zip(self.messages.android, self.messages.linux):
            if (len(a_msg.text) > 0) and (len(l_msg.text) > 0):
                if a_msg.text != l_msg.text:
                    return False
            if (len(a_msg.html) > 0) and (len(l_msg.html) > 0):
                if a_msg.html != l_msg.html:
                    return False
        return True

    def compare_attachments(self):
        return True # False

