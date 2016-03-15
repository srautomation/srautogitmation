import time
import crypt
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.platform.linux.applications.Leafpad.Leafpad import *

from logbook import Logger
log = Logger("SETTINGS")


class SettingsBaseTest(BaseTest):
    PRIVILAGE_USER="BigScreen"
    NEW_USER = "test_user1"
    OLD_PASS = "123qwezxc"#TODO how do we get the old password?
    NEW_PASS = "1@password"
    LANGUGE_CHECK = "قخمخق"
    VERIFY_PASS = NEW_PASS
    HINT = "1@password"
    pass_entries = [OLD_PASS, NEW_PASS, VERIFY_PASS, HINT]
    initialized = False
    
    #-------------------------------------------- def __init__(self,*args,**kv):
        #----------------------------------------------- BaseTest.__init__(self)
            
    
    def before(self):
        if not self.initialized :
            super(SettingsBaseTest, self).before()
            SettingsBaseTest.start_settings()
            self.initialized = True 
            
    
    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()

    
    def test_account_changeUser(self):
        slash.g.settings.account.enter()
        slash.g.settings.account.set_username(self.NEW_USER)
        assert slash.g.settings.account.get_username() == self.NEW_USER
        slash.g.settings.account.exit()


    def test_account_changePass(self):
        slash.g.settings.account.enter()
        slash.g.settings.account.change_pass(self.pass_entries)
        slash.g.settings.
        if len()
        self.checkPassword()
        slash.g.settings.account.exit()
         
    def checkPassword(self):
        time.sleep(2)
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = slash.g.settings._linux.shell.runCommandWithReturnValue(cmd)
        assert crypt.crypt(self.NEW_PASS,output) == output
    
    
    def test_language_and_keyboard(self):
        slash.g.settings.language_and_keyboard.enter()
        slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        time.sleep(5)
        self.checklanguage()
        slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        slash.g.settings.language_and_keyboard.exit()

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
   