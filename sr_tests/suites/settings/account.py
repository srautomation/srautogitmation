import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
import crypt
from logbook import Logger
log = Logger("ACCOUNT")


class AccountBaseTest(BaseTest):
    NEW_PASS = "123qwe!"
    NEW_USER = "test_user1"
    PRIVILAGE_USER="BigScreen"
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
        old_name = self.account.get_username()
        self.account.set_username(self.NEW_USER)
        assert self.account.get_username() == self.NEW_USER
        time.sleep(1)
        self.account.set_username(old_name) #cleanup

    @slash.skipped    
    def test_account_changePass(self):
        OLD_PASS = slash.g.sunriver.currentPass
        VERIFY_PASS = self.NEW_PASS
        HINT = "123qwe!"
        pass_entries = [OLD_PASS,self.NEW_PASS, VERIFY_PASS, HINT]
        self.account.change_pass(pass_entries)
        self.checkPassword()
        pass_entries = [self.NEW_PASS,OLD_PASS ,OLD_PASS, OLD_PASS] #cleanup
        self.account.change_pass(pass_entries)

    def checkPassword(self):
        time.sleep(2)
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = self.settings.linux.shell.runCommandWithReturnValue(cmd)
        assert crypt.crypt(self.NEW_PASS,output) == output
        slash.g.sunriver.currentPass = self.NEW_PASS
         
    def after(self):
        self.settings.stop()
