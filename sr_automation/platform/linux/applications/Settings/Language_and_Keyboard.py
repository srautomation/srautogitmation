
class Language_and_keyboard(object):

    KEYBOARD_SUBMENU = (500, 200)
    ADD_REMOVE_BUTTON = "Add / Remove Language"
    ADD_REMOVE_ARABIC = ()
    def __init__(self, settings):
        self._settings = settings

    def enter(self):
        self._app = self._settings.app
        self._settings.click_at_xy(self.KEYBOARD_SUBMENU)

    def add_keyboard_language(self):
        self._app.child(name=self.ADD_REMOVE_BUTTON).click()


    def remove_keyboard_language(self):
        pass

