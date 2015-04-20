from sr_tests.base.Base import BaseTest

import slash
import slash.log
import time
import os
import subprocess

class SwitchBaseTest(BaseTest):

    times_to_switch = 5

    def test_many_switches(self):
        for i in range(self.times_to_switch):
            slash.logger.info('Cycle #%s' % (i+1))
            slash.g.sunriver.switch_to_android.switch()
            time.sleep(5)
            slash.g.sunriver.desktop.switch_to_desktop()
            time.sleep(8)

    def test_switch(self):
        slash.g.sunriver.switch_to_android.switch()
        time.sleep(5)

