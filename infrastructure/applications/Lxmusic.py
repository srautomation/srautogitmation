import time
from Application import _Application

class Lxmusic(_Application):
    def __init__(self, linux):
        super(Lxmusic, self).__init__(linux, 'lxmusic')

    def play(self, track):
        app = self._dogtail.tree.root.application('lxmusic')
        app.child(track).point()
        time.sleep(3)
        app.child(track).doubleClick()

    def pause(self):
        app = self._dogtail.tree.root.application('lxmusic')
        app.child('Pause').point()
        time.sleep(2)
        app.child('Pause').click()
