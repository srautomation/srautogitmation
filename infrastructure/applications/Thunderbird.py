import datetime
from Application import _Application
import time

class Thunderbird(_Application):
    def __init__(self, linux):
        super(Thunderbird, self).__init__(linux, "thunderbird", dogtail_id = "Thunderbird")
        self._main_frame  = None
        self._compose_frame = None
        self._predicate = self._dogtail.predicate.GenericPredicate

    #-------------------------------------------
    # Mailbox files inspection
    def folder(self, name):
        mails = self._mailbox.mbox(name)
        for mail in mails:
            mail.sender     = mail['From']
            mail.to         = mail['To']
            mail.subject    = mail['Subject']
            mail.date       = datetime.datetime.strptime(mail['Date'].rsplit(" ", 1)[0], "%a, %d %b %Y %H:%M:%S %Z")
            
            mozilla_status = int(mail["X-Mozilla-Status"])
            mail.is_read    = (mozilla_status & 1)
            mail.is_starred = (mozilla_status & 4)
            mail.is_deleted = (mozilla_status & 8)

        return [mail for mail in mails if mail.is_deleted is False]

    def drafts(self):
        return self.folder("Drafts")

    def inbox(self):
        return self.folder("Inbox")

    def sent(self):
        return self.folder("Sent")

    def trash(self):
        return self.folder("Trash")

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
