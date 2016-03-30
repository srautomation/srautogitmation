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

   
    
    #------------------------------------- def test_language_and_keyboard(self):
        #------------------------ slash.g.settings.language_and_keyboard.enter()
        #- slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        #--------------------------------------------------------- time.sleep(5)
        #-------------------------------------------------- self.checklanguage()
        #- slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        #------------------------- slash.g.settings.language_and_keyboard.exit()

    def checklanguage(self):
        text = "aba"
        text_in_arabic="شﻻش" 
        leafpad = Leafpad(slash.g.sunriver.linux)
        leafpad.start()
        slash.g.settings.dogtail.rawinput.keyCombo('<Shift><Alt_L>') 
        leafpad.write_text(text,WriteMethod.Raw) #write in arabic 
        print leafpad.read_text()
        assert leafpad.read_text() == text_in_arabic
 
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
   