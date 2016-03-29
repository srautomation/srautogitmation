import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
import crypt
from logbook import Logger
log = Logger("ACCOUNT")


class AccountBaseTest(BaseTest):
    
    PRIVILAGE_USER="BigScreen"
    NEW_USER = "test_user1"
    OLD_PASS = "1@password"#TODO how do we get the old password?
    NEW_PASS = "123qwe!"
    VERIFY_PASS = NEW_PASS
    HINT = "123qwe!"
    pass_entries = [OLD_PASS, NEW_PASS, VERIFY_PASS, HINT]
    initialized = False
    
    def before(self):
        if not self.initialized:
            self.initialized = True
            super(AccountBaseTest, self).before()
            self.settings = Settings(slash.g.sunriver.linux)
            self.account = self.settings.account
        self.settings.start()
        self.account.enter()

    def test_account_changeUser(self):
        self.account.set_username(self.NEW_USER)
        assert self.account.get_username() == self.NEW_USER
        
    def test_account_changePass(self):
        self.account.change_pass(self.pass_entries)
        self.checkPassword()
        
    def checkPassword(self):
        time.sleep(2)
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = self.settings.linux.shell.runCommandWithReturnValue(cmd)
        print output
        assert crypt.crypt(self.NEW_PASS,output) == output
        print "succeed"
         
    def after(self):
        self.settings.stop()
