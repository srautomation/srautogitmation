from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
import time
from bunch import Bunch
import slash

from logbook import Logger
log = Logger("Search and App Launcher")

class LauncherBaseTest(BaseTest):
   
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

    def open_app_sidepanel(self, stimes = 3):
	log.info('Testing SidePanel Notification Popups')
	for i in range(stimes):
		slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control><Alt>l')
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(330,330)
                time.sleep(4)
    
    def close_app(self):
        log.info('close')
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(50,120, button=3)
        time.sleep(3)
        slash.g.sunriver.linux.ui.dogtail.rawinput.click(130,70)

    def open_contextual(self):
	log.info('Testing contexual menu')
	log.info('iconify')
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(50,120, button=3)
	time.sleep(3)
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(120, 320)
        time.sleep(3)
        #
	log.info('raise')	
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(50,120, button=3)
	time.sleep(3)
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(120,140)
        time.sleep(3)
        #
	log.info('maximize')
        slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(50,120, button=3)
	time.sleep(3)
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(120,240)
	time.sleep(3)
        #
        log.info('close')
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(50,120, button=3)
	time.sleep(3)
	slash.g.sunriver.linux.ui.dogtail.rawinput.doubleClick(130,70)

    def open_folders(self, folder_name):
	if folder_name == 'Files':
		log.info('Opening Files')
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(330,130)
	if folder_name == 'Pictures':
		log.info('Opening Pictures')
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(560,130)
	if folder_name == 'Videos':
		log.info('Opening Videos')
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(775,130)
	if folder_name == 'Music':
		log.info('Opening Music')
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(1000,130)

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
