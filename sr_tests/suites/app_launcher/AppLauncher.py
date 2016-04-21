import slash
import commands
from Base import LauncherBaseTest
import time
from logbook import Logger
from sr_automation.utils.ProcessManager import ProcessManager
log = Logger("App Launcher Suite")

class AppLaunchTest(LauncherBaseTest):

    @slash.hooks.session_start.register
    def start_AppLauncher():
        log.info('Starting "Search, App Launcher and Side Panel" Suite')

    def open_app_from_launcher(self, i_appName):
        self.open_from_applauncher_by_icon_name(i_appName)
        appPid = ProcessManager.convert_app_name_to_pid(i_appName)
        appOpened = ProcessManager.check_app_by_pid(appPid)
        slash.should.be(appOpened, True)

    def test_a_launcher(self):
        log.info('Verify Top Side of App Launcher')
        folder_list = ['Files', 'Pictures', 'Videos', 'Music']
        for folder in folder_list:
            self.open_from_applauncher_by_icon_name(folder)
            time.sleep(3)
        launcherWorks = self.assert_and_close_folders()
        slash.should.be(launcherWorks, True)

    def test_b_app_from_launcher(self):
        log.info('Contextual tests on app launched by app launcher')
        self.open_app_from_launcher('Galculator')
        time.sleep(3)
        contextualPassed = self.contextual_asserts_on_calc()
        slash.should.be(contextualPassed, True)

    def test_c_from_desktop(self):
        log.info('Contextual tests on app launched from desktop')
        ProcessManager.run_app_if_not_runnning("pcmanfm --desktop")
        openedFromDesktop = self.open_directory_from_desktop()
        time.sleep(3)
        slash.should.be(openedFromDesktop, True)

    def test_d_search(self):
        log.info('Search Chromium and launch')
        searchedChromium = self.search_chromium()
        time.sleep(3)
        slash.should.be(searchedChromium, True)

    def test_e_bad_search(self):
        log.info('Search bad text')
        searchedBadText = self.bad_search()
        time.sleep(3)
        slash.should.be(searchedBadText, True)

