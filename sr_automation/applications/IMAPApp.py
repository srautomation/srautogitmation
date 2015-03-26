import email
import time
from dateutil import parser
from bunch import Bunch

class IMAPApp(object):
    def __init__(self, linux):
        self._linux = linux
        self._imap_module = self._linux._rpyc.modules.imaplib
        self._imap = self._imap_module.IMAP4("localhost")
        self._key = self._read_key()

        self._email = None
        self._password = None
        self._folder = None
        self._count = None

    def _assert_result(self, result):
        assert result == "OK"

    def _read_key(self):
        return self._linux.shell.shell("cat /run/imapsmtp/key").stdout.read().strip()

    def choose_email(self, email, password=""):
        self._email = email
        self._password = password
        def authentication_callback(response):
            return "\x00{} {}\x00{}".format(email, self._key, password)
        result, _unused = self._imap.authenticate("PLAIN", authentication_callback)
        self._assert_result(result)
        return self

    def choose_folder(self, folder):
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
        _tmp = [x.split(" ", 3) for x in data]
        # dict indexed by uid
        self._flags = {int(x[2]): self.flags_string_to_bunch(x[3]) for x in _tmp}

        # for now, fetch all TODO: think about it
        uids_text = ','.join(map(str, self._flags.keys())) 
        result, data = self._imap.uid("fetch", uids_text, "(UID BODY[])") #)BODY.PEEK[HEADER.FIELDS (From To Cc Bcc Subject Date Message-ID Priority X-Priority References Newsgroups In-Reply-To Content-Type Reply-To)]")
        self._assert_result(result)
        # dict indexed by uid
        self._msgs = {int(x[0].split(" ", 3)[2]): email.message_from_string(x[1]) for x in data[::2]}
        return self
        #return data

    def messages(self):
        _messages = [Bunch(
            _uid  = uid,
            time  = parser.parse(mail["date"]),
            from_ = mail["from"],
            to    = mail["to"],
            cc    = mail["cc"],
            subject = mail["subject"],
            flags = self._flags[uid],
            body = Bunch(
                text = mail.get_payload()[0].get_payload(),
                html = mail.get_payload()[0].get_payload().decode('base64'),
                ),
            )
            for (uid, mail) in sorted(self._msgs.iteritems())]
        return _messages
