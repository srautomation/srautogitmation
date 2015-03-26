from sqlalchemy import *
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz
import time
from bunch import Bunch

from EmailGuiController import EmailGuiController

class AndroidMail(object):
    PATH_ANDROID_DB   = "/data/data/com.android.email/databases/EmailProvider.db"
    PATH_ANDROID_BODY = "/data/data/com.android.email/databases/EmailProviderBody.db"
    PATH_LOCAL_DB     = "/tmp/EmailProvider.db"
    PATH_LOCAL_BODY   = "/tmp/EmailProviderBody.db"

    def __init__(self, android):
        self._android = android
        self._email = None
        self._password = None
        self._folder = None

        self.gui = EmailGuiController(android.ui)

    def _pull_database(self):
        self._android.cmd("root")
        self._android.cmd("pull %s %s" % (AndroidMail.PATH_ANDROID_DB, AndroidMail.PATH_LOCAL_DB))
        self._android.cmd("pull %s %s" % (AndroidMail.PATH_ANDROID_BODY, AndroidMail.PATH_LOCAL_BODY))
    
    def choose_email(self, email, password=None):
        self._email = email
        self._password = password
        return self

    def choose_folder(self, folder):
        self._folder = folder
        return self

    def load(self):
        self._pull_database()
        Base = declarative_base()
        self._engine_db   = create_engine("sqlite:///%s" % AndroidMail.PATH_LOCAL_DB)
        self._engine_body = create_engine("sqlite:///%s" % AndroidMail.PATH_LOCAL_BODY)
        self._metadata_db   = MetaData(bind = self._engine_db)
        self._metadata_body = MetaData(bind = self._engine_body)
        time.sleep(2)

        class Account(Base):
            __table__ = Table("Account", self._metadata_db, autoload = True)
        self.Account = Account

        class Mailbox(Base):
            __table__ = Table("Mailbox", self._metadata_db, 
                    Column("accountKey", Integer, ForeignKey("Account._id")), 
                    autoload = True)
            account = relationship("Account")
        self.Mailbox = Mailbox

        class Message(Base):
            __table__ = Table("Message", self._metadata_db, 
                    Column("mailboxKey", Integer, ForeignKey("Mailbox._id")), 
                    Column("accountKey", Integer, ForeignKey("Account._id")),
                    autoload = True)
            account = relationship("Account")
            mailbox = relationship("Mailbox")
        self.Message = Message

        class Attachment(Base):
            __table__ = Table("Attachment", self._metadata_db,
                    Column("accountKey", Integer, ForeignKey("Account._id")),
                    Column("messageKey", Integer, ForeignKey("Message._id")),
                    autoload = True)
            account = relationship("Account")
            message = relationship("Message")
        self.Attachment = Attachment
        
        class Body(Base):
            __table__ = Table("Body", self._metadata_body, autoload = True)
        self.Body = Body
        
        self._session_db   = create_session(bind = self._engine_db)
        self._session_body = create_session(bind = self._engine_body)
        return self

    def query(self, obj):
        return self._session_db.query(obj)

    def messages(self):
        _messages = self._session_db.query(self.Message).join(self.Message.mailbox).filter(self.Mailbox.displayName == self._folder, self.Account.emailAddress == self._email)
        ids = [x._id for x in _messages]
        _bodies = self._session_body.query(self.Body).filter(
            self.Body.messageKey.in_(ids))
        _bodies = {m.messageKey: m for m in _bodies}
        messages = [Bunch(
            _uid  = m._id,
            time  = pytz.utc.localize(datetime.utcfromtimestamp(m.timeStamp / 1000.0)),
            from_ = m.fromList.split('\x02')[0],
            to    = m.toList,
            cc    = m.ccList,
            subject = m.subject,
            flags = Bunch(
                read       = (m.flagRead == 1),
                attachment = (m.flagAttachment == 1),
                favorite   = (m.flagFavorite == 1),
                loaded     = (m.flagLoaded == 1),
                ),
            body = Bunch(
                text = _bodies[m._id].textContent,
                html = _bodies[m._id].htmlContent,
                ),
            )
            for m in _messages]
        return messages
                         
    def send(self, to, subject, body, attachments=[]):
        self.gui.send(to, subject, body, attachments)
"""
a = AndroidMail(self.android).load()
print a.query(a.Message).filter(a.Message.flagAttachment == 1, a.Account.emailAddress == "barak@wizery.com", ).all()
print a.query(a.Message).count()
print [message.subject for message in a.query(a.Message).all()]
"""
