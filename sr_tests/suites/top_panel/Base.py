from sr_tests.base.Base import BaseTest
from sr_automation.utils.ImageTools import ImageTools
from sr_automation.utils.TimeUtils import TimeUtils
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
        if ImageStats.max_value > 0.9:
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
            errorMessage = i_MenuName+" is not opening the correct menu"
            assert OpenedMenu != False, errorMessage
        else:
            errorMessage = i_MenuName+" Icon missing"
            assert FoundIcon != False , errorMessage
    
    def test_clock(self):
        log.info("Verifying Clock Icon")
        TimeUtils.sync_time()
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
        for i in range(4):
            if str(current_time)[i] != displayed_time[i]:
                CorrectClock = False
        log.info("Current time is: "+str(current_time)+" While displayed time is: "+displayed_time)
        assert CorrectClock == True , "Time not displayed or incorrect time"

    def test_battery(self):
        log.info("Verifying Battery Icon")
        FoundIcon = self.find_icon_in_top_panel("Battery")
        assert FoundIcon != False , "Battery Icon missing"

    def test_switch_to_phone(self):
        log.info("Verifying Switch to Phone Icon")
        FoundIcon = self.find_icon_in_top_panel("SwitchToPhone")
        assert FoundIcon != False , "Switch to Phone Icon missing"

    def test_network_wifi(self):
        log.info("Verifying Network & Wi-Fi Icons")
        FoundIcon = self.find_icon_in_top_panel("NetworkWiFi")
        assert FoundIcon != False , "Missing or incorrect Network and WiFi Icons"
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(FoundIcon[1]+50, FoundIcon[0]+15)
        SignalStrength = self.find_icon_in_top_panel("SignalStrength")
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        assert SignalStrength != False , "Signal Strength does not appear or appears incorrect"

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
