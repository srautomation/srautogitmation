from Tester import Tester
import slash

class BaseTest(slash.Test):
    def before(self):
        self.tester = Tester()
        self.device = self.tester.device()
        self.device.start()
        self.linux = self.device.linux
        self.android = self.device.android

    def after(self):
        self.device.stop()

