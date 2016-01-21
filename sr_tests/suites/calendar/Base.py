from sr_tests.base.Base import BaseTest
from sr_automation.platform.android.applications.Calendar.GUI import AndroidCalendarGUI
from sr_automation.platform.android.applications.Calendar.Calendar import AndroidCalendar
from sr_automation.platform.linux.applications.Calendar.Calendar import LinuxCalendar
import slash 
import time

from bunch import Bunch
import slash

from logbook import Logger
log = Logger("CalendarBaseTest")


@slash.hooks.session_start.register
def calendar_start_sync():
    log.info("starting calendar")
   
    slash.g.calendar = Bunch( android = AndroidCalendar(slash.g.sunriver.android),
                              linux = LinuxCalendar(slash.g.sunriver.linux))    

    slash.g.events = Bunch( android = None,
                         linux = None)                    


class CalendarBaseTest(BaseTest):

    def before(self):
        super(CalendarBaseTest, self).before()
        self.calendar.android.load()

    def choose_calender(self, email, password=None):
        self.calendar.email = email
        self.calenaar.password = password
        self.calendar.android.choose_account(email, password)
        self.calendar.linux.choose_account(email, password)
        return self

    def load(self):
        self.calendar.android.load()
        time.sleep(5)
        self.events.android = self.calendar.android.events()
        self.events.linux = self.calendar.linux.events()

    def compare_all(self):
        slash.should.be(self.compare_count(), True)
        slash.should.be(len(self.compare_title()), 0)
        slash.should.be(len(self.compare_events_end_time()), 0)
        slash.should.be(len(self.compare_events_start_time()), 0)

    @property
    def calendar(self):
        return slash.g.calendar

    @property
    def events(self):
        return slash.g.events
 
    def compare_count(self):
        return len(self.events.android) == len(self.events.linux)

    def compare_title(self):
        return [i for (i, (a, l)) in enumerate(zip(self.events.android, self.events.linux)) if a.title != l.title]
                        
    def compare_events_end_time(self):
        return [i for (i, (a, l)) in enumerate(zip(self.events.android, self.events.linux)) if a.end != l.dtend]

    def compare_events_start_time(self):
        return [i for (i, (a, l)) in enumerate(zip(self.events.android, self.events.linux)) if a.start != l.dtstart]
