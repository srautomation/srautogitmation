from sqlalchemy import *
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.automap import automap_base
from datetime import datetime
import pytz
from bunch import Bunch
import time

from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


class AndroidContacts(object):
    PATH_ANDROID_DB = "/data/data/com.android.providers.contacts/databases/contacts2.db"
    PATH_LOCAL_DB   = "/tmp/contacts2.db"
    
    def __init__(self, android):
        self._android = android
        self._account = None

    def _pull_database(self):
        self._android.cmd("root")
        self._android.cmd("pull %s %s" % (AndroidContacts.PATH_ANDROID_DB, AndroidContacts.PATH_LOCAL_DB))

    def choose_account(self, account):
        self._account = account
        return self

    def load(self):
        self._pull_database()
        Base = declarative_base()
        self._engine_db   = create_engine("sqlite:///%s" % AndroidContacts.PATH_LOCAL_DB)
        self._metadata_db   = MetaData(bind = self._engine_db)
        time.sleep(2)

        class data(Base):
            __table__ = Table("data", self._metadata_db,
                    Column("_id", Integer, primary_key=True),
                    Column("package_id", Integer, ForeignKey("packages._id")),
                    Column("mimetype_id", Integer, ForeignKey("mimetypes._id")),
                    )
        self.data = data

        class accounts(Base):
            __table__ = Table("accounts", self._metadata_db,
                    Column("data_id", Integer, primary_key=True),
                    autoload=True)
        self.accounts = accounts

        class phone_lookup(Base):
            __table__ = Table("phone_lookup", self._metadata_db,
                    Column("data_id", Integer, primary_key=True),
                    Column("raw_contact_id", Integer, ForeignKey("raw_contacts._id")),
                    autoload=True)
        self.phone_lookup = phone_lookup

        class raw_contacts(Base):
            __table__ = Table("raw_contacts", self._metadata_db,
                    Column("account_id", Integer, ForeignKey("accounts._id")),
                    autoload=True,
                    extend_existing=True)
        self.raw_contacts = raw_contacts

        self._session_db = create_session(bind = self._engine_db)
        return self


    def query(self, obj):
        return self._session_db.query(obj)

    def contacts(self):
        _phones_query = self._session_db.query(self.phone_lookup)
        phones = {p.raw_contact_id: p.normalized_number for p in _phones_query}

        _contacts_query = self._session_db.query(self.raw_contacts)
        contacts = [Bunch(_id   = c._id,
                           name  = c.display_name,
                           phone = phones.get(c._id, ""),
                          )
                    for c in _contacts_query
                    ]
        return contacts
        #_events = self._session.query(self.Events).join(self.Events.calendars) #.filter(self.Mailbox.displayName == self._folder, self.Account.emailAddress == self._email)


if __name__ == "__main__":
    import sys; sys.path.append("../..")
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    contacts  = AndroidContacts(android)
    contacts.load()
    print contacts.contacts()
