import slash
from Base import LauncherBaseTest
import time
from logbook import Logger
log = Logger("StressBaseInsideTest")

class AppLaunchTest(LauncherBaseTest):

    @slash.hooks.session_start.register
    def start_AppLauncher():
        slash.g.stress_run = 1
        log.info('Opening AppLauncher')
        slash.g.cycle = 0

    def folders_open(self):
	folder_list = ['Files', 'Pictures', 'Videos', 'Music']
	for folder in folder_list:
		self.open_from_applauncher_by_icon_name(folder)
		time.sleep(4)

    def check_app_opened_from_launcher(self, i_appName):
        self.open_from_applauncher_by_icon_name(i_appName)
        appPid = self.convert_app_name_to_pid(i_appName)
        appOpened = self.check_app_by_pid(appPid)
        slash.should.be(appOpened, True)
        return appPid

    def test_launcher(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
	    self.folders_open()
            #assert like contextual
            self.close_all_apps()
            #assert like contextual
            time.sleep(3)
            app_name = 'Galculator'
            app_pid = self.check_app_opened_from_launcher(app_name)
	    self.contextual_on_calc()
	    time.sleep(7)
	    searchedChromium = self.search_chromium()
            slash.should.be(searchedChromium, True)
   	    slash.g.cycle +=1
	self.compare_cycle(slash.g.cycle, slash.g.stress_run)
