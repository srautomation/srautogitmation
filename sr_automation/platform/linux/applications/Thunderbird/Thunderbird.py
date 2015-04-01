import re
import datetime
from Application import _Application
import time
import os
import mailbox
import dateutil.parser
from rpyc.utils.classic import download_file
from bunch import Bunch


class Thunderbird(_Application):
    SQLITE_DB_NAME = "global-messages-db.sqlite"
    PATH_LOCAL = os.path.join("/tmp", SQLITE_DB_NAME)
    PROFILES_INI_PATTERN = re.compile("\[([^\s]+?)\][^\[]*?Name=([^\s]+?)$[^\[]*?Path=([^\s]+?)$", re.DOTALL | re.MULTILINE)

    def __init__(self, linux):
        super(Thunderbird, self).__init__(linux, "thunderbird", dogtail_id = "Thunderbird")
        self._main_frame  = None
        self._compose_frame = None
        self._predicate = self._dogtail.predicate.GenericPredicate
        self._profiles  = None
        self._mailboxes = None
        self._profile_path = None

    def _load_profiles(self):
        text = self._linux.shell.shell("cat ~/.thunderbird/profiles.ini").stdout.read()
        self._profiles = {name: path for (_, name, path) in Thunderbird.PROFILES_INI_PATTERN.findall(text)}
        return self._profiles

    def _find_mailboxes(self, profile):
        profile = "default" # TODO: fix
        self._profile_path = os.path.join(self._linux._rpyc.modules.os.path.expanduser("~"), ".thunderbird", self._profiles[profile])
        results = self._linux.shell.shell("find %s -name *.msf" % self._profile_path).stdout.readlines()
        results = [x[x.find("Mail"):].rsplit(".", 1)[0] for x in results]
        results = {x.rsplit("/", 1)[1]: x for x in results}
        self._mailboxes = results
        return self._mailboxes

    def _pull_mailbox(self, name):
        assert name in self._mailboxes.keys()
        remote_path = os.path.join(self._profile_path, self._mailboxes[name])
        local_path  = os.path.join("/tmp", name + ".mbox")
        remote_file = self._linux._rpyc.builtins.file(remote_path, "rb")
        local_file  = file(local_path, "wb")
        local_file.write(remote_file.read())
        remote_file.close()
        local_file.close()
        return local_path

    def _load_mailbox(self, name):
        mbox = mailbox.mbox(self._pull_mailbox(name)) 
        return mbox
            
    def messages(self, email, mailbox):
        self._find_mailboxes(email)
        mbox = self._load_mailbox(mailbox) 
        _messages = [Bunch(
            time  = dateutil.parser.parse(m["date"]),
            from_ = m["from"],
            to    = m["to"],
            cc    = None,
            subject = m["subject"],
            flags = Bunch(
                read    = (0 != int(m["X-Mozilla-Status"]) & 1),
                starred = (0 != int(m["X-Mozilla-Status"]) & 4),
                deleted = (0 != int(m["X-Mozilla-Status"]) & 8),
                attachment = False,
                favorite   = False,
                loaded     = False,
                ),
            body = Bunch(
                text = m.get_payload(),
                html = None,
                ),
            )
            for m in mbox]
        return _messages

    def load(self):
        self._load_profiles()
        return self

    #-------------------------------------------
    # GUI automation
    def start(self):
        super(Thunderbird, self).start()
        time.sleep(10) 
        self._main_frame = [x for x in self._app.findChildren(self._predicate(roleName = "frame")) if x.name.endswith("Mozilla Thunderbird")][0]

    def _folder(self, folder):
        try:
            self._item = [x for x in self._main_frame.findChildren(self._predicate(roleName = "list item")) if x.name.startswith(folder)][0]
        except IndexError as e:
            tab = [x for x in self._main_frame.findChildren(self._predicate(roleName = "page tab"))][0]
            tab.click()
            self._item = [x for x in self._main_frame.findChildren(self._predicate(roleName = "list item")) if x.name.startswith(folder)][0]
        self._item.click()
    
    def inbox(self):
        self._folder("Inbox")

    def drafts(self):
        self._folder("Drafts")

    def trash(self):
        self._folder("Trash")

    def mails(self):
        mails = []
        table = self._main_frame.child(roleName = "table")
        columns = [x.name for x in table.findChildren(self._predicate(roleName = "column header"))]
        for row in table.findChildren(self._predicate(roleName = "table row")):
            thread, starred, attachment, subject, unread, recipient, junk, date = [x.name for x in row.findChildren(self._predicate(roleName = "table cell"))]
            starred    = (starred == "Starred")
            attachment = (attachment == "Has Attachment")
            read       = not (unread == "Unread")
            junk       = (junk == "100")
            subject    = ["", subject][subject != "subjectCol"]
            recipient  = ["", recipient][recipient != "recipientCol"]
            mails.append(dict(zip(columns, (thread, starred, attachment, subject, read, recipient, junk, date))))
        return mails
    
    def search(self, text):
        search_text = [x for x in self._main_frame.findChildren(self._predicate(roleName = "entry")) if x.name.startswith("Search")][0]
        search_text.text = text
        self._app.keyCombo("<enter>")
        self._app.child("Open email as list").click()


    def compose(self):
        self._main_frame.child("Write").click()
        self._compose_frame = [x for x in self._app.findChildren(self._predicate(roleName = "frame")) if x.name.startswith("Write:")][0]
        class Compose(object):
            def to(_self, emails):
                self._compose_frame.child(name = "To:", roleName = "autocomplete").child(roleName = "entry").text = ",".join(emails)
                return _self
            
            def subject(_self, text):
                self._compose_frame.child(name = "Subject:", roleName = "entry").text = text
                return _self

            def body(_self, text):
                self._compose_frame.child(roleName = "document frame").text = text
                return _self

            def attach(_self, files_paths):
                for file_path in files_paths:
                    self._compose_frame.button("Attach").click()
                    attach_dialog = self._app.child(name = "Attach File(s)", roleName = "dialog")
                    attach_dialog.child("/").click()
                    attach_dialog.child(roleName = "text").text = file_path
                    attach_dialog.button("Open").click()
                return _self

            def save(_self):
                self._compose_frame.button("Save").click()
                return _self
        return Compose()
