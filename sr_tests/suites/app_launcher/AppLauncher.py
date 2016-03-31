import slash
from Base import LauncherBaseTest
import time
from logbook import Logger
from sr_automation.utils.ProcessManager import ProcessManager
log = Logger("StressBaseInsideTest")

class AppLaunchTest(LauncherBaseTest):

    @slash.hooks.session_start.register
    def start_AppLauncher():
        slash.g.stress_run = 1
        log.info('Opening AppLauncher')
        slash.g.cycle = 0

    def open_app_from_launcher(self, i_appName):
        self.open_from_applauncher_by_icon_name(i_appName)
        appPid = ProcessManager.convert_app_name_to_pid(i_appName)
        appOpened = ProcessManager.check_app_by_pid(appPid)
        slash.should.be(appOpened, True)

    def test_launcher(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
            folder_list = ['Files', 'Pictures', 'Videos', 'Music']
            for folder in folder_list:
                self.open_from_applauncher_by_icon_name(folder)
                time.sleep(3)
            self.assert_and_close_folders()
            time.sleep(3)
            self.open_app_from_launcher('Galculator')
	    time.sleep(3)
            self.contextual_on_calc()
	    time.sleep(3)
	    searchedChromium = self.search_chromium()
            time.sleep(3)
            slash.should.be(searchedChromium, True)
   	    slash.g.cycle +=1
	self.compare_cycle(slash.g.cycle, slash.g.stress_run)
