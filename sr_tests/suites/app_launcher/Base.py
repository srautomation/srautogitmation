from sr_tests.base.Base import BaseTest
from sr_automation.utils.ImageTools import ImageTools
import time
import getpass
import slash

from logbook import Logger
log = Logger("Search, App Launcher and Side Panel")

class LauncherBaseTest(BaseTest):

    m_username = getpass.getuser()
   
    def before(self):
        super(LauncherBaseTest, self).before()

    def open_launcher(self):
        log.info('Opening Launcher')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control><Alt>l')

    def open_search(self, i_value=None):
        log.info('Opening Search')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control><Alt>f')
        time.sleep(1)
        if i_value != None:
            slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(i_value)
   
    def open_directory_from_desktop(self):
        log.info('Creating empty file on desktop')
        automation_file = '/home/BigScreen/Desktop/File.txt'
        slash.g.sunriver.linux.ui.dogtail.procedural.os.mknod(automation_file)
        log.info('Testing Side panel from Desktop')
        snapshot = "Desktop_snapshot.png"
        desktop = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Desktop.png"
        sidebar = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Leafpad-sidebar.png"
        close_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close.png"
        time.sleep(2)
        folder = ImageTools.find_sub_image_in_image(snapshot, desktop)
        if folder.max_value > 0.9:
            slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(folder.max_location[1]+15, folder.max_location[0]+15)
        else:
            log.error('Unable to see file on desktop')
            return False
        time.sleep(1)
        sidebar_snap = ImageTools.find_sub_image_in_image(snapshot, sidebar)
        returnValue = False
        if sidebar_snap.max_value > 0.9:
            returnValue = True
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(sidebar_snap.max_location[1]+15, sidebar_snap.max_location[0]+15, button=3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        time.sleep(3)
        location = ImageTools.find_sub_image_in_image(snapshot, close_button)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(location.max_location[1]+15,location.max_location[0]+15)
        slash.g.sunriver.linux.ui.dogtail.procedural.os.remove(automation_file)
        return returnValue

    def search_chromium(self):
        log.info('Searching Chromium application')
        chromium = "/home/"+self.m_username+"/sr_automation/automation-screenshots/ChromiumSearch.png"
        close_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close.png"
        snapshot = "Search_snapshot.png"
        self.open_search('Chro')
        imageStats = ImageTools.find_sub_image_in_image(snapshot, chromium)
        time.sleep(1)
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Down>')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Enter>')
        sidebar = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Chromium-sidebar.png"
        time.sleep(3)
        sidebar_snap = ImageTools.find_sub_image_in_image(snapshot, sidebar)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(sidebar_snap.max_location[1]+15, sidebar_snap.max_location[0]+15, button=3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        time.sleep(1)
        location = ImageTools.find_sub_image_in_image(snapshot, close_button)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(location.max_location[1]+15,location.max_location[0]+15)
        found = False
        if imageStats.max_value > 0.9:
            found = True
        return found

    def bad_search(self):
        log.info('Searching non-existent text')
        bad_text = "/home/"+self.m_username+"/sr_automation/automation-screenshots/BadSearch.png"
        snapshot = "BadSearch_snap.png"
        self.open_search('NoTextExist')
        time.sleep(1)
        imageStats = ImageTools.find_sub_image_in_image(snapshot, bad_text)
        self.open_search()
        found = False
        if imageStats.max_value > 0.9:
            found = True
        return found

    def assert_and_close_folders(self):
        log.info('Closing all windows')
        closeall = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close-all.png"
        folders = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Folders.png"
        folders_ss = "Folders_snapshot.png"
        folders_pos = ImageTools.find_sub_image_in_image(folders_ss, folders)
        foundFolders = False
        if folders_pos.max_value > 0.9:
            foundFolders = True
        slash.should.be(foundFolders, True)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(folders_pos.max_location[1]+15,folders_pos.max_location[0]+15, button=3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        time.sleep(3)
        snapshot = "Close_snapshot.png"
        location = ImageTools.find_sub_image_in_image(snapshot, closeall)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(location.max_location[1]+15,location.max_location[0]+15)
        folders_pos = ImageTools.find_sub_image_in_image(folders_ss, folders)
        foundFolders = False
        if folders_pos.max_value > 0.9:
            foundFolders = True
        slash.should.be(foundFolders, False)
        return True

    def sidebar_manipulation(self, i_x, i_y, i_button=1):
        snapshot = "sidebar_snapshot.png"
        interface = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Galculator-interface.png"
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(i_x,i_y,i_button)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        imageStats = ImageTools.find_sub_image_in_image(snapshot, interface)
        found = False
        if imageStats.max_value > 0.9:
            found = True
        return found

    def contextual_asserts_on_calc(self):
	log.info('Testing contexual menu on Galculator')
        sidebar_icon = "/home/"+self.m_username+"/sr_automation/automation-screenshots/Galculator-sidebar.png"
        snapshot = "Contextual_snapshot.png"
        location = ImageTools.find_sub_image_in_image(snapshot, sidebar_icon)
        x = location.max_location[1] + 15
        y = location.max_location[0] + 15
        log.info('Minimize from sidebar')
        found = self.sidebar_manipulation(x,y)
        slash.should.be(found, False)
        log.info('Restore from sidebar by left click')
        found = self.sidebar_manipulation(x,y)
        slash.should.be(found, True)
        log.info('Minimize from sidebar')
        found = self.sidebar_manipulation(x,y)
        slash.should.be(found, False)
        log.info('Restore from sidebar by right click')
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(x,y, button=3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        open_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/open.png"
        openLocation = ImageTools.find_sub_image_in_image(snapshot, open_button)
        found = self.sidebar_manipulation(openLocation.max_location[1]+15,openLocation.max_location[0]+15)
        slash.should.be(found, True)
        log.info('Close from sidebar by right click')
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(x,y, button=3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.absoluteMotion(0,0)
        close_button = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close.png"
        closeLocation = ImageTools.find_sub_image_in_image(snapshot, close_button)
        found = self.sidebar_manipulation(closeLocation.max_location[1]+15,closeLocation.max_location[0]+15)
        slash.should.be(found, False)
        return True

    def open_from_applauncher_by_icon_name(self, i_folderName):
        log.info('Opening '+i_folderName+' from App Launcher')
        self.open_launcher()
        time.sleep(3)
        screenshot = "/home/"+self.m_username+"/sr_automation/automation-screenshots/"+i_folderName+".png"
        snapshot = i_folderName + '_snapshot.png'
        location = ImageTools.find_sub_image_in_image(snapshot, screenshot)
        x = location.max_location[1] + 15
        y = location.max_location[0] + 15
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(x,y)
