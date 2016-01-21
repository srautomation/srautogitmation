import time

class Calc(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("libreoffice --calc --norestore")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("soffice")

    def stop(self):
        if self._process.is_running():
            self._linux.cmd("killall oosplash")
        if self._process.is_running():
            self._process.terminate()

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
