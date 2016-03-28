from sr_automation.platform.linux.applications.Settings.Settings_submenu import Settings_submenu
import time

class Language_and_keyboard(Settings_submenu):

    KEYBOARD_SUBMENU = (500, 200)
    ADD_REMOVE_BUTTON = "Add / Remove Language"
    LANGUAGE_ARABIC = (840, 440)
    APPLY_CHANGES = "Apply Changes"

    def __init__(self, settings):
        super(Language_and_keyboard, self).__init__(settings, self.KEYBOARD_SUBMENU)

    def add_remove_keyboard_language(self):
        self._open_supported_language_menu()
        self._settings.click_at_xy(self.LANGUAGE_ARABIC)
        time.sleep(3)
        self._app.child(name=self.APPLY_CHANGES).click()

    def _open_supported_language_menu(self):
        self._app.child(name=self.ADD_REMOVE_BUTTON).grabFocus()
        self._app.child(name=self.ADD_REMOVE_BUTTON).click()
        
        
         
        
        




