from sr_automation.platform.linux.applications.dialogs.DialogOpen import DialogOpen
import time

class Impress(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("libreoffice --impress --norestore")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("soffice")

    def stop(self):
        if self._process.is_running():
            self._linux.cmd("killall oosplash")
        if self._process.is_running():
            self._process.terminate()

    def open(self, doc):
        app = self._app
        app.child('Open', 'push button').click()
        time.sleep(4)
        DialogOpen.open(app, doc)

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

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    impress = Impress(sunriver.linux)
    impress.start()
    import IPython
    IPython.embed()
    impress.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()



