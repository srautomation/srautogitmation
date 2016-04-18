from sr_tests.base.Base import BaseTest
from sr_automation.utils.TimeUtils import TimeUtils
from sr_automation.utils.ImageTools import ImageTools
from datetime import datetime
import getpass
import time
import slash
import os

from logbook import Logger
from time import sleep
log = Logger("Alarm Clock")

class AlarmBaseTest(BaseTest):
       
    m_username = getpass.getuser()
    m_ActionsPos = None

    def before(self):
        super(AlarmBaseTest, self).before()    
    
    def set_alarm_for_next_interval(self):
        log.info("setting alarm for the next interval")
        self.sunriver.desktop.openSpecificApp('Clock')
        self.sunriver.android.ui(className="android.widget.ImageView", description="Alarm").click()
        self.sunriver.android.ui(resourceId="com.android.deskclock:id/fab").click()
        self.sunriver.android.ui(resourceId="android:id/minutes").click()
        timeToSet = TimeUtils.get_next_interval()
        for text in timeToSet:
            slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(text)
        self.sunriver.android.ui(resourceId="android:id/button1").click()
        return TimeUtils.format_time(timeToSet)
    
    def set_snooze_period(self, i_TimeToSet):
        SnoozePossibilities = range(1,31)
        RequestedSnooze = str(i_TimeToSet)
        if i_TimeToSet not in SnoozePossibilities:
            log.error("Unable to set snooze for: "+RequestedSnooze)
            return 0
        log.info("setting snooze period for: "+RequestedSnooze)
        self.sunriver.desktop.openSpecificApp('Clock')
        self.sunriver.android.ui(className="android.widget.ImageView", description="Clock").click()
        self.sunriver.android.ui(resourceId="com.android.deskclock:id/menu_button").click()
        self.sunriver.android.ui(text="Settings").click()
        self.sunriver.android.ui(text="Snooze length").click()
        if not self.sunriver.android.ui(text=RequestedSnooze).exists:
            for snooze in SnoozePossibilities:
                title = str(snooze)
                if self.sunriver.android.ui(text=title).exists:
                    LowerNum = snooze
                    break
            if LowerNum >= i_TimeToSet:
                NumToClick = LowerNum
                modifier = -1
            else:
                NumToClick = LowerNum + 2
                modifier = 1
            while NumToClick != i_TimeToSet:
                ClickTitle = str(NumToClick)
                self.sunriver.android.ui(text=ClickTitle).click()
                time.sleep(1)
                NumToClick += modifier
        self.sunriver.android.ui(text=RequestedSnooze).click()
        self.sunriver.android.ui(text="OK").click()
        
    def AlarmRaised(self):
        IconPath = "/home/"+self.m_username+"/sr_automation/automation-screenshots/AlarmActions.png"
        Snapshot = "AlarmSnapshot.png"
        ActionsStats = ImageTools.find_sub_image_in_image(Snapshot, IconPath)
        found = False
        if ActionsStats.max_value > 0.9:
            self.m_ActionsPos = (ActionsStats.max_location[0], ActionsStats.max_location[1])
            found = True
        return found
    
    def clickAction(self, i_Action):
        if i_Action is 'Snooze':
            IconPath = "/home/"+self.m_username+"/sr_automation/automation-screenshots/AlarmSnooze.png"
        elif i_Action is 'Dismiss':
            IconPath = "/home/"+self.m_username+"/sr_automation/automation-screenshots/AlarmDismiss.png"
        else:
            slash.add_error('Action '+i_Action+' does not exist!')
        Snapshot = "ActionSnapshot.png"
        self.sunriver.linux.ui.dogtail.rawinput.click(self.m_ActionsPos[1]+15, self.m_ActionsPos[0]+15)
        ActionsStats = ImageTools.find_sub_image_in_image(Snapshot, IconPath)
        if ActionsStats.max_value > 0.9:
            self.sunriver.linux.ui.dogtail.rawinput.click(ActionsStats.max_location[1]+15, ActionsStats.max_location[0]+15)
        else:
            slash.add_error('Unable to find '+i_Action+' button!')
      
    def test_alarm(self):
        TimeUtils.sync_time()
        self.sunriver.vnc.OpenVnc()
        self.set_snooze_period(1)
        alarmTime = self.set_alarm_for_next_interval()
        time.sleep(4)
        self.sunriver.android.ui.press.home()
        self.sunriver.vnc.CloseVnc()
        log.info("Waiting for alarm...")
        while datetime.now().time() < alarmTime:
            time.sleep(1)
        slash.should.be(self.AlarmRaised(), True)
        self.clickAction('Snooze')
        time.sleep(60)
        slash.should.be(self.AlarmRaised(), True)
        self.clickAction('Dismiss')