from infrastructure.applications.Application import _Editor
import time
import dogtail

class Impress(_Editor):
    def __init__(self, linux):
        super(Impress, self).__init__(linux, 'libreoffice --impress --norestore', 'killall oosplash')

    def open(self, doc):
        app = self._dogtail.tree.root.application('soffice')
        app.child('Open', 'push button').click()
        time.sleep(4)
        app.child(doc).point()
        time.sleep(1)
        app.child(doc).doubleClick()

    def start_slideshow(self, mouse_clicks):
        attempts = 0
        while attempts < 5: #TODO: change workaround 
            attempts += 1
            try:
                app = self._dogtail.tree.root.application('soffice')
                break
            except Exception as e:
                if e.__class__.__name__ == 'gi._glib.GError':
                    time.sleep(1)
                else: 
                    raise e
        btn = app.child('Start from first Slide', 'push button')
        btn.point()
        time.sleep(2)
        btn.click()
        time.sleep(3)
        for click in range(mouse_clicks):
            self._dogtail.rawinput.pressKey('enter')
            time.sleep(2)
        self._dogtail.rawinput.pressKey('esc')
