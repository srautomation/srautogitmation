from sr_automation.platform.linux.applications.dialogs.DialogOpen import DialogOpen
import time
from logbook import Logger
log = Logger("LibreOffice")


class Writer(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self, option=''):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._dogtail.procedural.run("libreoffice --writer --norestore %s"%option)
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("soffice")
        
    def stop(self):
        self._linux.cmd("killall oosplash")

    def open(self, doc):
        app = self._app
        app.child('Open').click()
        time.sleep(2)
        DialogOpen.open(app, doc)

    def set_bold(self):
        app = self._app
        app.child('Edit').click()
        time.sleep(1)
        app.child('Edit').child('Select All').point()
        time.sleep(1)
        app.child('Edit').child('Select All').click()
        time.sleep(2)
        app.child('Bold').click()

    def set_italic(self):
        app = self._app
        app.child('Edit').click()
        time.sleep(1)
        app.child('Edit').child('Select All').point()
        time.sleep(1)
        app.child('Edit').child('Select All').click()
        time.sleep(2)
        app.child('Italic').click()

    def write_text(self, text):
        app = self._app
        app.child(roleName = 'paragraph').text = text

    def save_as(self, file_name='file'):
        app = self._app
        app.child(name='Save').click()
        app.child(roleName='dialog').child(roleName='text').text = file_name
        app.child(roleName='dialog').child(roleName='push button', name='Save').click()
       
    def choose_slide(self,slide_number=1):
        app = self._app
        app.child(name='Slide %s'%slide_number).click()
