from sr_tests.base.Base import BaseTest
from sr_automation.utils.ImageTools import ImageTools
import time
import getpass
import slash
import datetime

from logbook import Logger
log = Logger("Top Panel Suite")

class PanelBaseTest(BaseTest):

    m_username = getpass.getuser()

    def before(self):
        super(PanelBaseTest, self).before()
    
    def find_icon_in_top_panel(self, i_IconName):
        IconPath = "/home/"+self.m_username+"/sr_automation/automation-screenshots/TopPanel"+i_IconName+".png"
        Snapshot = "IconSnapshot.png"
        found = False
        ImageStats = ImageTools.find_sub_image_in_image(Snapshot, IconPath)
        if ImageStats.max_value > 0.8:
            found = (ImageStats.max_location[0], ImageStats.max_location[1])
        return found

    def template_verification(self, i_IconName, i_MenuName):
        log.info("Verifying "+i_MenuName+" Icon")
        FoundIcon = self.find_icon_in_top_panel(i_IconName)
        if FoundIcon is not False:
            slash.g.sunriver.linux.ui.dogtail.rawinput.click(FoundIcon[1]+15,FoundIcon[0]+15)
            slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
            time.sleep(1)
            OpenedMenu = self.find_icon_in_top_panel(i_IconName+"Menu")
            slash.g.sunriver.linux.ui.dogtail.rawinput.click(0,0)
            slash.should.not_be(OpenedMenu, False)
        else:
            log.error(i_MenuName+" Icon missing")
            slash.should.not_be(FoundIcon, False)
    
    def test_clock(self):
        log.info("Verifying Clock Icon")
        NotifPath = "/home/"+self.m_username+"/sr_automation/automation-screenshots/TopPanelNotifications.png"
        Snapshot = "ClockSnapshot.png"
        current_time = datetime.datetime.now().time()
        NotifStats = ImageTools.find_sub_image_in_image(Snapshot, NotifPath)
        x_min = int(NotifStats.max_location[1]-75)
        x_max = int(NotifStats.max_location[1])
        ClockCrop = {
                    "y_min" : 0,
                    "y_max" : 50,
                    "x_min" : x_min,
                    "x_max" : x_max,
                    "z_min": 0,
                    "z_max" : 3
                    }
        displayed_time = ImageTools.ocr_image(Snapshot, ClockCrop)
        CorrectClock = True
        for i in range(2):
            if str(current_time)[i] != displayed_time[i]:
                CorrectClock = False
        slash.should.be(CorrectClock, True)

    def test_battery(self):
        log.info("Verifying Battery Icon")
        FoundIcon = self.find_icon_in_top_panel("Battery")
        slash.should.not_be(FoundIcon, False)

    def test_switch_to_phone(self):
        log.info("Verifying Switch to Phone Icon")
        FoundIcon = self.find_icon_in_top_panel("SwitchToPhone")
        slash.should.not_be(FoundIcon, False)

    def test_network_wifi(self):
        log.info("Verifying Network & Wi-Fi Icons")
        FoundIcon = self.find_icon_in_top_panel("NetworkWiFi")
        slash.should.not_be(FoundIcon, False)

    def test_search(self):
        self.template_verification("Search", "Search")

    def test_app_launcher(self):
        self.template_verification("Applications", "App Launcher")

    def test_user_menu(self):
        self.template_verification("UserMenu", "User Menu")

    def test_language(self):
        self.template_verification("Language", "Language")

    def test_notifications(self):
        self.template_verification("Notifications", "Notifications")

    def test_phone_app(self):
        if slash.g.sunriver.vnc.isVNCOpen():
            slash.g.sunriver.vnc.CloseVnc()
        self.template_verification("Phone_App", "Phone App")
        slash.g.sunriver.vnc.CloseVnc()
    
    def test_bluetooth(self):
        self.template_verification("Bluetooth", "Bluetooth")
