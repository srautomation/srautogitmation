import time
from Application import _Application

class Lxmusic(_Application):
    def __init__(self, linux):
        super(Lxmusic, self).__init__(linux, 'lxmusic')

    def play(self, track):
        app = self._app
        app.child(track).point()
        time.sleep(3)
        app.child(track).doubleClick()

    def pause(self):
        app = self._app
        app.child('Pause').point()
        time.sleep(2)
        app.child('Pause').click()

    def stop(self):
        app = self._app
        app.child('File').click()
        time.sleep(2)
        app.child('Close').click()
