import slash
from Base import LauncherBaseTest
import time
from logbook import Logger
from sr_automation.utils.ProcessManager import ProcessManager
log = Logger("App Launcher Suite")

class AppLaunchTest(LauncherBaseTest):

    def before(self):
        super(AppLaunchTest, self).before()

    def open_app_from_launcher(self, i_appName):
        self.open_from_applauncher_by_icon_name(i_appName)
        appPid = ProcessManager.convert_app_name_to_pid(i_appName)
        appOpened = ProcessManager.check_app_by_pid(appPid)
        assert appOpened == True , "Unable to open "+i_appName+" from App Launcher"

    def test_launcher(self):
        log.info('Verify Top Side of App Launcher')
        folder_list = ['Files', 'Pictures', 'Videos', 'Music']
        for folder in folder_list:
            self.open_from_applauncher_by_icon_name(folder)
            time.sleep(2)
        launcherWorks = self.assert_and_close_folders()
        assert launcherWorks == True , "Unable to find or open the icons in the top of the App Launcher"

    def test_contextual_tests_from_launcher(self):
        log.info('Contextual tests on app launched by app launcher')
        self.open_app_from_launcher('Galculator')
        contextualPassed = self.contextual_asserts_on_calc()
        assert contextualPassed == True , "Error in contextual tests on app from launcher"

    def test_contextual_tests_from_desktop(self):
        log.info('Contextual tests on app launched from desktop')
        DesktopRunning = ProcessManager.verify_app_runnning("pcmanfm --desktop")
        assert DesktopRunning == True , "Desktop not running, aborting test"
        log.info('Creating empty file on desktop')
        automation_file = '/home/BigScreen/Desktop/File.txt'
        self.sunriver.linux.ui.dogtail.procedural.os.mknod(automation_file)
        log.info('Testing Side panel from Desktop')
        desktop = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Desktop.png"
        sidebar = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Leafpad-sidebar.png"
        close_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close.png"
        time.sleep(2)
        DesktopLocation = self.give_image_location_if_found(desktop)
        assert DesktopLocation != False , "Unable to see file on desktop"
        self.sunriver.linux.ui.dogtail.rawinput.doubleClick(DesktopLocation[1]+15, DesktopLocation[0]+15)
        time.sleep(2)
        SidebarLocation = self.give_image_location_if_found(sidebar)
        assert SidebarLocation != False , "Unable to see the file in the sidebar"
        self.sunriver.linux.ui.dogtail.rawinput.click(SidebarLocation[1]+15, SidebarLocation[0]+15, button=3)
        self.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        CloseLocation = self.give_image_location_if_found(close_button)
        assert CloseLocation != False , "Unable to close"
        self.sunriver.linux.ui.dogtail.rawinput.click(CloseLocation[1]+15,CloseLocation[0]+15)
        self.sunriver.linux.ui.dogtail.procedural.os.remove(automation_file)

    def test_search_chromium(self):
        log.info('Search Chromium and launch it')
        chromium = "/home/"+self.m_username+"/sr_automation/automation-screenshots/ChromiumSearch.png"
        close_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close.png"
        self.open_search('Chro')
        time.sleep(2)
        ChromiumLocation = self.give_image_location_if_found(chromium)
        assert ChromiumLocation != False , "Unable to open search for chromium"
        self.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Down>')
        self.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Enter>')
        sidebar = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Chromium-sidebar.png"
        time.sleep(4)
        SidebarLocation = self.give_image_location_if_found(sidebar)
        assert SidebarLocation != False , "Unable to see Chromium in sidebar"
        self.sunriver.linux.ui.dogtail.rawinput.click(SidebarLocation[1]+15, SidebarLocation[0]+15, button=3)
        self.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        CloseLocation = self.give_image_location_if_found(close_button)
        assert CloseLocation != False , "Unable to close"
        self.sunriver.linux.ui.dogtail.rawinput.click(CloseLocation[1]+15,CloseLocation[0]+15)

    def test_search_invalid_text(self):
        log.info('Search invalid text')
        bad_text = "/home/"+self.m_username+"/sr_automation/automation-screenshots/BadSearch.png"
        self.open_search('NoTextExist')
        time.sleep(4)
        BadSearchLocation = self.give_image_location_if_found(bad_text)
        assert BadSearchLocation != False , "Unable to see an invalid search results"
        self.open_search()
        
    def test_search_scrollbar(self):
        log.info('Verify search scroll bar')
        scrollbar = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Scrollbar.png"
        self.open_search('*')
        time.sleep(2)
        ScrollbarLocation = self.give_image_location_if_found(scrollbar)
        self.open_search()
        assert ScrollbarLocation != False , "Error with scrolling in search menu"
        
    def test_search_close_by_click(self):
        log.info('Verifying search closes on clickoutside')
        self.open_search()
        time.sleep(2)
        self.sunriver.linux.ui.dogtail.rawinput.click(0,0)
        search = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Search.png"
        SearchLocation = self.give_image_location_if_found(search)
        if SearchLocation == False:
            self.open_search()
        assert SearchLocation == False , "Search window still open"