import time
from sr_automation.platform.linux.applications.Settings.Account import Account
from sr_automation.platform.linux.applications.Settings.Language_and_Keyboard import Language_and_keyboard
from sr_automation.platform.linux.applications.Settings.Sound import Sound
from sr_automation.platform.linux.applications.Application import _Application


class Settings(_Application):

    APP_NAME = "sunriversettings"
    KILL_APP = "killall -9 " + APP_NAME
    ACCOUNT_SUBMENU = "Account"
    BACK_BUTTON_LOCATION = (80, 80)

    def __init__(self, linux):
        super(Settings, self).__init__(linux, start_cmd=self.APP_NAME,stop_cmd =self.KILL_APP,dogtail_id=self.APP_NAME)
        self._account = Account(self)
        self._language_and_keyboard = Language_and_keyboard(self)
        self._sound = Sound(self)

    @property
    def Settings(self):
        return self.app

    @property
    def account(self):
        return self._account
    
    @property
    def sound(self):
        return self._sound
    
    @property
    def language_and_keyboard(self):
        return self._language_and_keyboard

    def return_from_submenu(self):
        self.click_at_xy(self.BACK_BUTTON_LOCATION)


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


