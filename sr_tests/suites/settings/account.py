import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Account import Account

from logbook import Logger
log = Logger("ACCOUNT")


class AccountBaseTest(BaseTest):
    NEW_USER = "test_user"

    def before(self):
        super(AccountBaseTest, self).before()
        AccountBaseTest.start_account()

    @staticmethod
    def start_account():
        slash.g.account = Account()
        slash.g.account.start()

    def test_changeUsername(self):
        slash.g.settings.account.enter()
        slash.g.settings.account.set_username(self.NEW_USER)

    def after(self):
        slash.g.account.stop()
