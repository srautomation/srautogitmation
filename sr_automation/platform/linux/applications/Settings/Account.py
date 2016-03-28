#TODO: ACCount needs to inherite from Settings_submenu
from gi.overrides.keysyms import slash
import time
class Account(object):

    ACCOUNT_SUBMENU = "Account"
    DEFAULT_NAME = "Big Screen"
    CHANGE_PASSWORD_BUTTON = "Change Password"
    SUBMIT_PASSWORD_BUTTON = "Submit Changes"
    CANCEL_BUTTON = "Cancel"
    SAVE_BUTTON = "Save"

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
        time.sleep(3)
        assert len(self._settings._find_children(self._app, name="Dialog")) == 0, "wrong old password" #wrong password dialog opened
            

    def set_username(self, name=DEFAULT_NAME):
        self._app.child(roleName="text").text = name
        self._app.child(name=self.SAVE_BUTTON).click()
    
    def get_username(self):
        return self._app.child(roleName="text").text
        
    def upload_pic(self):
        pass

    def get_pass_entries_location(self):
        pass_entries_location = self._app.child(name=self.CHANGE_PASSWORD_BUTTON, roleName="label").parent.parent
        return self._settings._find_children(pass_entries_location, roleName="text")

    def exit(self):
        self._settings.return_from_submenu()

