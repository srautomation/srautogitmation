from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings


from logbook import Logger
log = Logger("SETTINGS")


class SettingsBaseTest(BaseTest):

    def before(self):
        super(SettingsBaseTest, self).before()
        SettingsBaseTest.start_settings()

    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()

    def test_account(self):
        slash.g.settings.account.start()
        slash.g.settings.account.change_username("test4")
        slash.g.settings.account.change_pass("blabla")

    def after(self):
        #slash.g.settings.stop()
        pass

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
