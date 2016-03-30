from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.utils.ImageTools import ImageTools
import time
import getpass
from bunch import Bunch
import slash
import signal

from logbook import Logger
log = Logger("Search and App Launcher")

class LauncherBaseTest(BaseTest):

    m_username = getpass.getuser()
   
    def before(self):
        super(LauncherBaseTest, self).before()
	
    def open_launcher(self):
        log.info('Opening Launcher')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control><Alt>l')

    def open_search(self, value= None):
	log.info('Opening search')
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control><Alt>f')
	if value != None:
		slash.g.sunriver.linux.ui.dogtail.rawinput.typeText(value)
    
    def search_chromium(self):
        log.info('Searching Chromium application')
        chromium = "/home/"+self.m_username+"/sr_automation/automation-screenshots/ChromiumSearch.png"
        snapshot = "Search_snapshot.png"
        self.open_search('Chro')
        imageStats = ImageTools.find_sub_image_in_image(snapshot, chromium)
        self.open_search()
        found = False
        if imageStats.max_value > 0.9:
            found = True
        return found

    def close_all_apps(self):
        log.info('Closing all windows')
        closeall = "/home/"+self.m_username+"/sr_automation/automation-screenshots/close-all.png"
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(50,120, button=3)
        time.sleep(3)
        snapshot = "Close_snapshot.png"
        location = ImageTools.find_sub_image_in_image(snapshot, closeall)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(location.max_location[1]+15,location.max_location[0]+15)

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

    def contextual_on_calc(self):
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
    
    #TODO: move it to the appropriate class
    def convert_app_name_to_pid(self, i_appName):
        cmd = "ps -ef | grep -i "+i_appName+" |grep -v grep |awk '{print $2}'"
        appPid = slash.g.sunriver.linux.shell.runCommandWithReturnValue(cmd)
        log.info(i_appName+"'s PID is "+appPid)
        return int(appPid)

    #TODO: move it to the appropriate class
    def check_app_by_pid(self, i_appPid):
        try:
            slash.g.sunriver.linux.ui.dogtail.procedural.os.kill(i_appPid, 0)
        except OSError:
            return False
        else:
            return True

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
