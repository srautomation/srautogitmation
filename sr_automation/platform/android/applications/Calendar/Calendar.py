from sqlalchemy import *
from sqlalchemy.orm import create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import pytz
from bunch import Bunch
import time
import IPython


class AndroidCalendar(object):
    PATH_ANDROID_DB = "/data/data/com.android.providers.calendar/databases/calendar.db"
    PATH_LOCAL_DB   = "/tmp/calendar.db"
    
    def __init__(self, android):
        self._android = android
        self._account = None

    def _pull_database(self):
        self._android.cmd("root")
        self._android.cmd("pull %s %s" % (AndroidCalendar.PATH_ANDROID_DB, AndroidCalendar.PATH_LOCAL_DB))

    def choose_account(self, account):
        self._account = account
        return self

    def load(self):
        self._pull_database()
        Base = declarative_base()
        self._engine_db = create_engine("sqlite:///%s" % AndroidCalendar.PATH_LOCAL_DB)
        self._metadata_db = MetaData(bind = self._engine_db)

        class CalendarCache(Base):
            __table__ = Table("CalendarCache", self._metadata_db, autoload = True)
        self.CalendarCache = CalendarCache

        class Attendees(Base):
            __table__ = Table("Attendees", self._metadata_db,
                    Column("event_id", Integer, ForeignKey("Events._id")),
                    autoload = True)
        self.Attendees = Attendees

        class Reminders(Base):
            __table__ = Table("Reminders", self._metadata_db,
                    Column("event_id", Integer, ForeignKey("Events._id")),
                    autoload = True)
        self.Reminders = Reminders

        class CalendarAlerts(Base):
            __table__ = Table("CalendarAlerts", self._metadata_db,
                    Column("event_id", Integer, ForeignKey("Events._id")),
                    autoload = True)
        self.CalendarAlerts = CalendarAlerts

        class ExtendedProperties(Base):
            __table__ = Table("ExtendedProperties", self._metadata_db,
                    Column("event_id", Integer, ForeignKey("Events._id")),
                    autoload = True)
        self.ExtendedProperties = ExtendedProperties

        class Colors(Base):
            __table__ = Table("Colors", self._metadata_db, # Maybe add acount_name reference
                    autoload = True)
        self.Colors = Colors

        class Calendars(Base):
            __table__ = Table("Calendars", self._metadata_db,
                    autoload = True)
        self.Calendars = Calendars

        class Events(Base):
            __table__ = Table("Events", self._metadata_db,
                    Column("_id", Integer, primary_key=True),
                    Column("calendar_id", Integer, ForeignKey("Calendars._id")),
                    Column("title", String),
                    Column("eventLocation", String),
                    Column("description", String),
                    Column("dtstart", Integer),
                    Column("dtend", Integer),
                    Column("eventTimezone", String),
                    Column("organizer", String),
                    )
            calendars = relationship("Calendars")
        self.Events = Events

        class EventsRawTimes(Base):
            __table__ = Table("EventsRawTimes", self._metadata_db,
                    autoload = True)
        self.EventsRAwTimes = EventsRawTimes

        class Instances(Base):
            __table__ = Table("Instances", self._metadata_db,
                    Column("event_id", Integer, ForeignKey("Events._id")),
                    autoload = True)
        self.Instances = Instances

        class CalendarMetaData(Base):
            __table__ = Table("CalendarMetaData", self._metadata_db,
                    autoload = True)
        self.CalendarMetaData = CalendarMetaData

        self._session_db = create_session(bind = self._engine_db)
        return self
    
    def query(self, obj):
        return self._session_db.query(obj)

    def events(self):
        _events = self._session_db.query(self.Events).join(self.Events.calendars) #.filter(self.Mailbox.displayName == self._folder, self.Account.emailAddress == self._email)
        events = [Bunch(
            _id         = e._id,
            title       = e.title,
            description = e.description,
            organizer   = e.organizer,
            start       = time.gmtime(e.dtstart / 1000),
            end         = time.gmtime([e.dtend, 0][e.dtend is None]   / 1000),
            )
            for e in _events]
        return events


if __name__ == "__main__":
    import sys; sys.path.append("../..")
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    calendar  = AndroidCalendar(android)
    calendar.load()
    print calendar.events()
    IPython.embed()
