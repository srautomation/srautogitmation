import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings


from logbook import Logger
log = Logger("SETTINGS")


class SettingsBaseTest(BaseTest):

    NEW_USER = "test_user"
    OLD_PASS = "?????" #TODO how do we get the old password?
    NEW_PASS = "1@password"
    VERIFY_PASS = NEW_PASS
    HINT = "1@password"
    pass_entries = [OLD_PASS, NEW_PASS, VERIFY_PASS, HINT]

    def before(self):
        super(SettingsBaseTest, self).before()
        SettingsBaseTest.start_settings()

    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()

    def test_account(self):
        slash.g.settings.account.enter()
        slash.g.settings.account.change_username(self.NEW_USER)
        slash.g.settings.account.change_pass(self.pass_entries)
        slash.g.settings.account.exit()

    
    def test_language_and_keyboard(self):
        #slash.g.settings.language_and_keyboard.enter 
        pass

    def after(self):
        time.sleep(3)
        slash.g.settings.stop()
        pass

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
