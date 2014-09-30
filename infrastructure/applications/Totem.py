import time
from Application import _Application

class Totem(_Application):
    def __init__(self, linux):
        super(Totem, self).__init__(linux, "totem")

    def open(self, movie):
        app = self._dogtail.tree.root.application('totem')
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
        app = self._dogtail.tree.root.application('totem')
        app.child(name = 'Play / Pause', roleName = 'push button').point()
        time.sleep(2)
        app.child(name = 'Play / Pause', roleName = 'push button').click()
