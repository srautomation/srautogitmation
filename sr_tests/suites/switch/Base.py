from sr_tests.base.Base import BaseTest
import slash
import time

class SwitchBaseTest(BaseTest):

    times_to_switch = 50

    def test_switch(self):
        for i in range(self.times_to_switch):
            slash.logger.info('Cycle #%s' % (i+1))
            slash.g.sunriver.switch_to_android.switch()
            time.sleep(4)
            slash.should.be(self.sunriver.desktop.is_desktop_running(), False)
            slash.g.sunriver.desktop.switch_to_desktop()
            time.sleep(4)
            slash.should.be(self.sunriver.desktop.is_desktop_running(), True)
