

class Account(object):

    ACCOUNT_SUBMENU = "Account"
    DEFAULT_NAME = "Big Screen"
    CHANGE_PASSWORD_BUTTON = "Change Password"
    SUBMIT_PASSWORD_BUTTON = "Submit Changes"
    CANCEL_BUTTON = "Cancel"
    SAVE_BUTTON = "Save"
    EXIT_BUTTON_LOCATION = (80, 80)

    def __init__(self, settings):
        self._settings = settings

    def enter(self):
        self._app = self._settings.app
        self._app.child(name=self.ACCOUNT_SUBMENU).click()

    def change_pass(self, _pass_entries):
        self._app.child(name=self.CHANGE_PASSWORD_BUTTON).click()
        pass_entries = self.get_pass_entries_location()
        for i in range(4):
            pass_entries[i].click()
            pass_entries[i].text = _pass_entries[i]
        self._app.child(name=self.SUBMIT_PASSWORD_BUTTON).click()

    def change_username(self, name=DEFAULT_NAME):
        self._app.child(roleName="text").text = name
        self._app.child(name=self.SAVE_BUTTON).click()

    def upload_pic(self):
        pass

    def get_pass_entries_location(self):
        pass_entries_location = self._app.child(name=self.CHANGE_PASSWORD_BUTTON, roleName="label").parent.parent
        return self._settings._find_children(pass_entries_location, roleName="text")

    def exit(self):
        self._settings.click_at_xy(self.EXIT_BUTTON_LOCATION)

