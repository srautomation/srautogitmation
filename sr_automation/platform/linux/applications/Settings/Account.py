

class Account(object):

    ACCOUNT_SUBMENU = "Account"
    DEFAULT_NAME = "Big Screen"
    CHANGE_PASSWORD_BUTTON = "Change Password"
    CANCEL_BUTTON = "Cancel"
    SAVE_BUTTON = "Save"

    def __init__(self, settings):
        self._settings = settings

    def start(self):
        self._app = self._settings.app
        self._app.child(name=self.ACCOUNT_SUBMENU).click()
        self._dogtail = self._settings.dogtail
        self._settings._linux.shell.cmd('sniff')

    def change_pass(self, new_pass):
        self._app.child(name=self.CHANGE_PASSWORD_BUTTON).click()
        self._app.child(name=self.CANCEL_BUTTON).click()

    def change_username(self, name=DEFAULT_NAME):
        self._app.child(roleName="text").text = name
        self._app.child(name=self.SAVE_BUTTON).click()

    def upload_pic(self):
        pass
