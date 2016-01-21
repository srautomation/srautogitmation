from sr_automation.platform.linux.applications.dialogs.DialogOpen import DialogOpen
import time

class Writer(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("libreoffice --writer --norestore")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("soffice")

    def stop(self):
        if self._process.is_running():
            self._linux.cmd("killall oosplash")
        if self._process.is_running():
            self._process.terminate()

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

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    writer = Writer(sunriver.linux)
    writer.start()
    writer.open("/etc/sysctl.conf")
    import IPython
    IPython.embed()
    writer.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()



