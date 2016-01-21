from sr_tests.suites.calendar.Base import CalendarBaseTest
from sr_automation.platform.android.applications.Calendar.GUI import AndroidCalendarGUI
import slash
import slash.log
import IPython
import time
import loremipsum

class AndroidCalendarEvent(CalendarBaseTest):
    calendar_conf = slash.config.sr.calendar
    number_of_events=50
    
    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.calendar.androidGUI = AndroidCalendarGUI(slash.g.sunriver.android)
 
    def before(self):
        super(AndroidCalendarEvent, self).before()        
        slash.g.sunriver.switch_to_android.switch()
        self.load()
        

    def after(self):
        time.sleep(10)
        self.load()
        self.compare_all()
        super(AndroidCalendarEvent, self).after()
         
    #def test_create_number_of_events(self):
     #   for i in range(self.number_of_events):
      #      slash.g.calendar.androidGUI.create_event(self.calendar_conf.name, self.calendar_conf.location)
        
    def test_event_and_delete(self):
        for i in range(10):
            slash.logger.info("cycle #%s" % (i + 1))
            slash.logger.info('creating events')
            for j in range(4):
                slash.g.calendar.androidGUI.create_event(self.calendar_conf.name, self.calendar_conf.location)
            slash.logger.info('deleting random events')
            for j in range(3):
                slash.g.calendar.androidGUI.delete_random_event()

