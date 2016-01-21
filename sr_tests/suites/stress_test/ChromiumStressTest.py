from sr_automation.platform.linux.applications.Browser.Browser import Chromium
from Base import StressBaseTest
import time
import slash

class ChromiumStressTest(StressBaseTest):

    @slash.hooks.session_start.register
    def start_chromium():
        slash.g.chromium = Chromium(slash.g.sunriver.linux)
        slash.g.stress_run = 500
        slash.g.cycle = 0

    def before(self):
        super(ChromiumStressTest, self).before()

    def test_stress(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
            slash.g.chromium.start()
            slash.g.chromium.open_youtube_video("watch?v=zLiR9OsqJa8")
            time.sleep(15) # allow video loading
            slash.g.chromium.pause_video()
            time.sleep(5)
            slash.g.chromium.play_video()
            slash.g.chromium.youtube_fullscreen()
            time.sleep(5)
            slash.g.chromium.escape()
            slash.g.chromium._driver.execute_script("window.open('http://www.cnn.com');")
            time.sleep(6) # let the website upload
            for i in range(4):
                slash.g.chromium.switch_tab()
	    slash.g.chromium.stop()
            slash.g.cycle = i           

    def after(self):
        self.compare_cycle(slash.g.stress_run, slash.g.cycle+1)
