import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Account import Account

from logbook import Logger
log = Logger("ACCOUNT")


class AccountBaseTest(BaseTest):

    def before(self):
        super(AccountBaseTest, self).before()
        AccountBaseTest.start_account()

    @staticmethod
    def start_account():
        slash.g.account = Account()
        slash.g.account.start()

    def test_account(self):
        time.sleep(5)
        slash.g.account.change_pass('yaniv')

    def after(self):
        slash.g.account.stop()
