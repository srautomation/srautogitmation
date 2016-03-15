import os.popen
import time
import crypt.crypt
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings


from logbook import Logger
import cmd
log = Logger("SETTINGS")


class SettingsBaseTest(BaseTest):
    PRIVILAGE_USER="BigScreen"
    NEW_USER = "test_user1"
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

    
    def test_account_changeUser(self):
        slash.g.settings.account.enter()
        slash.g.settings.account.set_username(self.NEW_USER)
        assert slash.g.settings.account.get_username() == "test"
       
    
    def test_account_changePass(self):
        slash.g.settings.account.change_pass(self.pass_entries)
        self.checkPassword() 
        slash.g.settings.account.exit()   
         
    def checkPassword(self):
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = os.popen(cmd).read()
        assert crypt.crypt(self.NEW_PASS,output) == output
    
    
    def test_language_and_keyboard(self):
        slash.g.settings.language_and_keyboard.enter()
        slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        time.sleep(3)
        slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
    
    def after(self):
        time.sleep(3)
        slash.g.settings.stop()
        pass

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
