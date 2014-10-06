from infrastructure.applications.Application import _Editor
import time

class Writer(_Editor):
    def __init__(self, linux):
        super(Writer, self).__init__(linux, 'libreoffice --writer --norestore', 'killall oosplash')

    def open(self, doc):
        app = self._dogtail.tree.root.application('soffice')
        app.child('Open').click()
        time.sleep(4)
        app.child(doc).point()
        time.sleep(1)
        app.child(doc).doubleClick()

    def set_bold(self):
        app = self._dogtail.tree.root.application('soffice')
        app.child('Edit').click()
        time.sleep(1)
        app.child('Edit').child('Select All').point()
        time.sleep(1)
        app.child('Edit').child('Select All').click()
        time.sleep(2)
        app.child('Bold').click()

    def set_italic(self):
        app = self._dogtail.tree.root.application('soffice')
        app.child('Edit').click()
        time.sleep(1)
        app.child('Edit').child('Select All').point()
        time.sleep(1)
        app.child('Edit').child('Select All').click()
        time.sleep(2)
        app.child('Italic').click()
