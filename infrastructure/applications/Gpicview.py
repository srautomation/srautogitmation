import time
from Application import _Application

class Gpicview(_Application):
    def __init__(self, linux):
        super(Gpicview, self).__init__(linux, 'gpicview')

    def open(self, photo):
        " photo must be in /root "
        app = self._dogtail.tree.root.application('gpicview')
        app.child('Open').point()
        time.sleep(2)
        app.child('Open').click()
        time.sleep(4)
        app.child('root').point()
        time.sleep(2)
        app.child('root').click()
        time.sleep(3)
        app.child(photo).point()
        time.sleep(2)
        app.child(photo).doubleClick()

    def next_photo(self):
        app = self._dogtail.tree.root.application('gpicview')
        app.child('Forward').point()
        time.sleep(2)
        app.child('Forward').click()

    def zoom_in(self):
        app = self._dogtail.tree.root.application('gpicview')
        app.child('Zoom In').point()
        time.sleep(2)
        app.child('Zoom In').click()
