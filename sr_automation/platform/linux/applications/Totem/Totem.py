import time
from Application import _Application

class Totem(_Application):
    def __init__(self, linux):
        self._linux = linux
    
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("totem")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("totem")

    def stop(self):
        if self._process.is_running():
            self._process.terminate()

    def open(self, movie):
        app = self._app
        app.child('Movie').point()
        time.sleep(1)
        app.child('Movie').click()
        time.sleep(2)
        app.child('Open...').point()
        time.sleep(1)
        app.child('Open...').click()
        time.sleep(2)
        app.child('Home').click()
        time.sleep(2)
        app.child(movie).doubleClick()

    def toggle_play_pause(self):
        app = self._app
        app.child(name = 'Play / Pause', roleName = 'push button').point()
        time.sleep(2)
        app.child(name = 'Play / Pause', roleName = 'push button').click()
