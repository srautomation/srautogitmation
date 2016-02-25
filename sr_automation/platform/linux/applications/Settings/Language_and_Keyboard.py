
class Language_and_keyboard(object):

    KEYBOARD_SUBMENU = ""

    def __init__(self, settings):
        self._settings = settings

    def enter(self):
        self._app = self._settings.app
        self._app.child(name=self.KEYBOARD_SUBMENU).click()

    def add_keyboard_language(self):
        pass

    def remove_keyboard_language(self):
        pass

