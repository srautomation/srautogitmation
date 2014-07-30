from infrastructure.BaseTest import BaseTest
import time
import slash

class Example1(BaseTest):
    def test_waiting_window(self):
        result = None
        with self.tester.timeout(120):
            self.device.linux.ui.run("/usr/bin/leafpad")
            result = self.device.linux.ldtp.waittillguiexist("*frm*")
        slash.should.equal(result, 1)

