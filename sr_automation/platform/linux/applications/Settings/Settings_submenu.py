
class Settings_submenu(object):

    def __init__(self, settings , submenu):
        self._settings = settings
        self._SUBMENU = submenu
        self._dogtail = settings.dogtail

    def enter(self):
        self._app = self._settings.app
        self._settings.click_at_xy(self._SUBMENU)

    def exit(self):
        self._settings.return_from_submenu()
