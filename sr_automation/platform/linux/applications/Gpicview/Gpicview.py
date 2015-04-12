import time

class Gpicview(object):
    def __init__(self, linux):
        self._linux = linux
    
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("gpicview")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("gpicview")

    def stop(self):
        if self._process.is_running():
            self._process.terminate()

    def open(self, photo):
        " photo must be in /root "
        app = self._app
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
        app = self._app
        app.child('Forward').point()
        time.sleep(2)
        app.child('Forward').click()

    def zoom_in(self):
        app = self._app
        app.child('Zoom In').point()
        time.sleep(2)
        app.child('Zoom In').click()

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    gpicview = Gpicview(sunriver.linux)
    gpicview.start()
    import IPython
    IPython.embed()
    gpicview.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()



