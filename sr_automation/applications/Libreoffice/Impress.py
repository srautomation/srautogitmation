from sr_automation.applications.Application import _Editor
from os import path
import time
import dogtail

class Impress(_Editor):
    def __init__(self, linux):
        super(Impress, self).__init__(linux, 'libreoffice --impress --norestore', 'killall oosplash', 'soffice')

    def open(self, doc):
        app = self._app
        app.child('Open', 'push button').click()
        time.sleep(4)
        self._open(doc)

    def start_slideshow(self, mouse_clicks):
        app = self._app
        btn = app.child('Start from first Slide', 'push button')
        btn.point()
        time.sleep(2)
        btn.click()
        time.sleep(3)
        for click in range(mouse_clicks):
            self._dogtail.rawinput.pressKey('enter')
            time.sleep(2)
        self._dogtail.rawinput.pressKey('esc')
