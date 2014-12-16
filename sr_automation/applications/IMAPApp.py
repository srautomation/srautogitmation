from imapclient import IMAPClient
import email
import time


class IMAPApp(object):
    def __init__(self, linux):
        self._linux = linux
        self._imap = None
        self._info = None
        self._email = None
        self._password = None
        self._folder = None
        self._ids  = None
        self._msgs = None


    def choose_email(self, email, password=None):
        self._email = email
        self._password = password
        self._imap = IMAPClient("imap.gmail.com", ssl=True) #ssl=False) #TODO: fix this with real IMAPApp
        self._imap.login(self._email, self._password)
        return self

    def choose_folder(self, folder):
        self._folder = folder
        self._imap.select_folder(self._folder)
        return self

    def load(self):
        self._ids  = self._imap.search("ALL")
        self._msgs = self._imap.fetch(self._ids, ["FLAGS", "RFC822"])
        return self

    def messages(self):
        emails = [(m["FLAGS"], email.message_from_string(m["RFC822"])) for m in self._msgs.values()[1:]]
        _messages = [Bunch(
            time  = dateutil.parser.parse(m[1]["date"]),
            from_ = m[1]["from"],
            to    = m[1]["to"],
            cc    = None,
            subject = m[1]["subject"],
            flags = Bunch(
                read    = ("\\Seen" in m[0]),
                starred = ("\\Flagged" in m[0]),
                deleted = ("\\Deleted" in m[0]),
                attachment = False,
                favorite   = False,
                loaded     = False,
                ),
            body = Bunch(
                text = m[1].get_payload()[0].get_payload(),
                html = m[1].get_payload()[1].get_payload(),
                ),
            )
            for m in emails]
        return _messages
