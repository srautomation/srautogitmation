from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
from sr_automation.utils.ImageTools import ImageTools
import time
from bunch import Bunch
import getpass
import slash

from logbook import Logger
log = Logger("Phone App and Basic Remoting")

class PhoneAppBaseTest(BaseTest):
    
    m_username = getpass.getuser()

    def before(self):
        super(PhoneAppBaseTest, self).before()

    def test_peripherals_and_messaging(self):
        slash.g.sunriver.vnc.OpenVnc()
        HomeIcon = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Home.png"
        MessagingIcon = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Messaging.png"
        NewMessageIcon = "/home/"+self.m_username+"/sr_automation/automation-screenshots/NewMessage.png"
        NotifAlert = "/home/"+self.m_username+"/sr_automation/automation-screenshots/NotificationAlert.png"
        ReplyButton = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Reply.png"
        SendMessageButton = "/home/"+self.m_username+"/sr_automation/automation-screenshots/SendMessage.png"
        Snapshot = "MessagingSnapshot.png"
        log.info("Sending click on Home button")
        Home = ImageTools.find_sub_image_in_image(Snapshot, HomeIcon)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Home.max_location[1]+15, Home.max_location[0]+15)
        time.sleep(1)
        log.info("Sending click on Messaging Icon")
        Messaging = ImageTools.find_sub_image_in_image(Snapshot, MessagingIcon)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Messaging.max_location[1]+15, Messaging.max_location[0]+15)
        time.sleep(1)
        log.info("Sending click on New Message Button")
        NewMessage = ImageTools.find_sub_image_in_image(Snapshot, NewMessageIcon)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(NewMessage.max_location[1]+15, NewMessage.max_location[0]+15)
        MyNumber = "0547884440" #need to replace with correct phone number
        time.sleep(2)
        log.info("Typing message")
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(MyNumber)
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Enter>')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Tab>')
        slash.g.sunriver.linux.ui.dogtail.rawinput.typeText("Well look here, once I press this button here, time will flow 5 seconds backwards")
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Enter>')
        time.sleep(3)
        log.info("Sending click on Notification Button")
        Notification = ImageTools.find_sub_image_in_image(Snapshot, NotifAlert)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Notification.max_location[1]+15, Notification.max_location[0]+15)
        time.sleep(1)
        log.info("Sending click on reply button")
        Reply = ImageTools.find_sub_image_in_image(Snapshot, ReplyButton)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Home.max_location[1]+15, Home.max_location[0]+15)
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Notification.max_location[1]+15, Notification.max_location[0]+15)
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(Reply.max_location[1]+15, Reply.max_location[0]+15)
        time.sleep(1)
        SendMessage = ImageTools.find_sub_image_in_image(Snapshot, SendMessageButton)
        TestPassed = False
        if SendMessage.max_value > 0.9:
            TestPassed = True
        slash.should.be(TestPassed, True)

    def test_phone_calls(self):
        log.warn("Phone call automated test is not implemented yet")
