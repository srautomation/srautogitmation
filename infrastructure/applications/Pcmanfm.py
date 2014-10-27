from Application import _Application
import time

class Pcmanfm(_Application):
    def __init__(self, linux):
        super(Pcmanfm, self).__init__(linux, 'pcmanfm')

    def goto(self, dir):
        app = self._app
        app.child(roleName = 'text').text = dir
        time.sleep(3)
        app.child('Jump to').click()
