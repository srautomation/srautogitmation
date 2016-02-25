import time
from sr_automation.platform.linux.applications.Settings.Account import Account
from sr_automation.platform.linux.applications.Application import _Application


class Settings(_Application):

    APP_NAME = "sunriversettings"
    KILL_APP = "killall " + APP_NAME
    ACCOUNT_SUBMENU = "Account"

    def __init__(self, linux):
        super(Settings, self).__init__(linux, start_cmd=self.APP_NAME, stop_cmd=self.KILL_APP, dogtail_id=self.APP_NAME)
        self._account = Account(self)
        #self._language_and_keyboard = Language_and_keyboard(self)

    @property
    def Settings(self):
        return self.app

    @property
    def account(self):
        return self._account


if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    settings = Settings(sunriver.linux)
    settings.start()
    settings.goto("/root")
    import IPython
    IPython.embed()
    settings.stop()

    sunriver.stop()


