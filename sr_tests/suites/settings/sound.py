from sr_tests.base.Base import BaseTest
import slash

from logbook import Logger
log = Logger("ACCOUNT")


class SoundBaseTest(BaseTest):
    
    
    
    def before(self):
        if not self.initialized :
            super(SettingsBaseTest, self).before()
            SettingsBaseTest.start_settings()
            self.initialized = True 
            
    
    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()