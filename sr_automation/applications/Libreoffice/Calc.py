from sr_automation.applications.Application import _Editor
import time

class Calc(_Editor):
    def __init__(self, linux):
        super(Calc, self).__init__(linux, 'libreoffice --calc --norestore', 'killall oosplash', 'soffice')

    '''
    def open(self, doc):
        app = self._dogtail.tree.root.application('soffice')
        app.child('File').click()
        time.sleep(2)
        app.child('File').child('Open...').click()
        time.sleep(4)
        app.child(doc).point()
        time.sleep(1)
        app.child(doc).doubleClick()
    '''

    def start(self, doc):
        super(Calc, self).start(doc)

    def capitalize(self):
        app = self._app
        app.child('Edit').click()
        time.sleep(1)
        app.child('Edit').child('Select All').click()
        time.sleep(2)
        app.child('Format').click()
        time.sleep(1)
        app.child('Format').child('Change Case').click()
        time.sleep(1)
        app.child('Format').child('Change Case').child('UPPERCASE').click()
        time.sleep(1)
