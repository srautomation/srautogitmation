import slash
from Base import LauncherBaseTest
import time
from logbook import Logger
log = Logger("StressBaseInsideTest")

class AppLaunchTest(LauncherBaseTest):

    @slash.hooks.session_start.register
    def start_AppLauncher():
        slash.g.stress_run = 3
        log.info('Opening AppLauncher')
        slash.g.cycle = 0

    def folders_open(self):
	folder_list = ['Files', 'Pictures', 'Videos', 'Music']
	for folder in folder_list:
		self.open_launcher()
		self.open_folders(folder)
		time.sleep(4)


    def test_launcher(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
	    self.folders_open()
	    self.open_contextual()
	    self.open_search('Chro')
	    time.sleep(7)
	    self.open_app_sidpanel()
   	    slash.g.cycle +=1
	self.compare_cycle(slash.g.cycle, slash.g.stress_run)
	
	 

