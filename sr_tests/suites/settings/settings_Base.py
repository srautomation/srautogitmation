from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from logbook import Logger
log = Logger("SETTINGS")


@slash.hooks.session_start.register
def initialize_settings():
    if not hasattr(slash.g.sunriver, 'settings'):
        slash.g.sunriver.settings = Settings(slash.g.sunriver.linux)

class SettingsBaseTest(BaseTest):
 
    def before(self):
            super(SettingsBaseTest, self).before()
    
    def after(self):
        self.settings.stop()
        
    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)


if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    SettingsBaseTest = SettingsBaseTest(sunriver.linux)
    import IPython
    IPython.embed()   