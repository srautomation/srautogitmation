from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.platform.linux.applications.Leafpad.Leafpad import *
from sr_tests.suites.settings.account import AccountBaseTest
from logbook import Logger
log = Logger("SETTINGS")

class SettingsBaseTest(BaseTest):
 
    LANGUGE_CHECK = "قخمخق"
    initialized = False
    
    
    def before(self):
        if not self.initialized :
            super(SettingsBaseTest, self).before()
            SettingsBaseTest.start_settings()
            self.initialized = True 
    
    def test_account(self):
        self.Account_test = AccountBaseTest()
            
    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()


    def after(self):
        time.sleep(3)
        slash.g.settings.return_from_submenu()
        

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)


if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    SettingsBaseTest = SettingsBaseTest(sunriver.linux)
    import IPython
    IPython.embed()
   