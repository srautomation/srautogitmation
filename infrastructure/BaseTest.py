from gevent import monkey; monkey.patch_all(aggressive = False)
from Tester import Tester
import slash

class BaseTest(slash.Test):
    def before(self):
        self.tester = Tester()
        self.device = self.tester.device("MedfieldB60440E1")
        self.device.start()

    def after(self):
        self.device.stop()

