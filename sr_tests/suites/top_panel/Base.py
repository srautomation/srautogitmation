from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
from sr_automation.utils.ImageTools import ImageTools
import time
import getpass
from bunch import Bunch
import slash

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
            slash.should.not_be(OpenedMenu, False)
        else:
            log.error(i_MenuName+" Icon missing")
            slash.should.not_be(FoundIcon, False)

    def test_battery(self):
        log.info("Verifying Battery Icon")
        FoundIcon = self.find_icon_in_top_panel("Battery")
        slash.should.not_be(FoundIcon, False)

    def test_switch_to_phone(self):
        log.info("Verifying Switch to Phone Icon")
        FoundIcon = self.find_icon_in_top_panel("SwitchToPhone")
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
        self.template_verification("Phone_App", "Phone App")
    
    def test_bluetooth(self):
        self.template_verification("Bluetooth", "Bluetooth")
