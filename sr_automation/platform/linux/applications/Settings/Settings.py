import time
from sr_automation.platform.linux.applications.Settings.Account import Account


class Settings(object):

    APP_NAME = "sunriversettings"
    KILL_APP = "killall " + APP_NAME
    ACCOUNT_SUBMENU = "Account"

    def __init__(self, linux):
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail
        self._account = Account(self)

    def start(self):
        self._linux.shell.os_system(self.KILL_APP)
        self._process = self._dogtail.procedural.run(self.APP_NAME)
        time.sleep(9)
        self.app = self._dogtail.tree.root.application(self.APP_NAME)

    def stop(self):
        self._dogtail.procedural.run(self.KILL_APP)

    @property
    def Settings(self):
        return self.app

    @property
    def dogtail(self):
        return self._dogtail

    @property
    def account(self):
        return self._account

    def goto(self, menu_button):
        self.app.child(name=menu_button).click()





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


