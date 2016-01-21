from sr_automation.platform.linux.applications.parole.parole import parole
from Base import StressBaseTest
import time
import slash

class ParoleStressTest(StressBaseTest):

    @slash.hooks.session_start.register
    def start_parole():
        slash.g.parole = parole(slash.g.sunriver.linux)
        slash.g.parole.start()
        slash.g.stress_run = 2000
        slash.g.cycle = 0

    def before(self):
        super(ParoleStressTest, self).before()

    def test_stress(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
            if i==0:
                slash.g.parole.open_media('h264_gopro_running_dog.mp4')
                slash.g.parole.toggle_play_pause()
                slash.g.parole.stop()
                slash.g.cycle = i
            else:
                time.sleep(5)
                slash.g.parole.start()
                slash.g.parole.open_media('h264_gopro_running_dog.mp4')
                slash.g.parole.toggle_play_pause()
                slash.g.parole.stop()
                slash.g.cycle = i

    def after(self):
        self.compare_cycle(slash.g.stress_run, slash.g.cycle+1)
