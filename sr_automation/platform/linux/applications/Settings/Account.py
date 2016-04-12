from sr_automation.platform.linux.applications.Settings.Settings_submenu import Settings_submenu
class Account(Settings_submenu):

    DEFUALT_P = "1@password"
    DEFAULT_NAME = "Big Screen"
    CHANGE_PASSWORD_BUTTON = "Change Password"
    SUBMIT_PASSWORD_BUTTON = "Submit Changes"
    CANCEL_BUTTON = "Cancel"
    SAVE_BUTTON = "Save"
    
    ACCOUNT_SUBMENU =(200,200) 

    def __init__(self, settings):
        super(Account, self).__init__(settings, self.ACCOUNT_SUBMENU)

    def change_password_click(self):
        self._app.child(name=self.CHANGE_PASSWORD_BUTTON).click()

    def change_pass(self, _pass_entries):
        self.change_password_click()
        assert (self._app.child(name=self.SUBMIT_PASSWORD_BUTTON).sensitive) == False, "submit changes is not greyed-out" # check Submit changes is greyed-out
        pass_entries = self.get_pass_entries_location()
        for i in range(4):
            pass_entries[i].click()
            pass_entries[i].text = _pass_entries[i]
        self._app.child(name=self.SUBMIT_PASSWORD_BUTTON).click()
        self._dogtail.utils.doDelay(3)
        assert len(self._settings._find_children(self._app, name="Dialog")) == 0, "wrong old password" #wrong password dialog opened
            
    def write_in_textbox(self,value):
        self._app.child(roleName="text").text = value

    def set_username(self, name=DEFAULT_NAME):
        self.write_in_textbox(name)
        self._dogtail.utils.doDelay(1)
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

