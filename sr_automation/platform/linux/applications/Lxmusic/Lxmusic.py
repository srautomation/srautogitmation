import time

class Lxmusic(object):
    def __init__(self, linux):
        self._linux = linux
    
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("lxmusic")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("lxmusic")

    def stop(self):
        if self._process.is_running():
            self._process.terminate()

    def play(self, track):
        app = self._app
        app.child(track).point()
        time.sleep(3)
        app.child(track).doubleClick()

    def pause(self):
        app = self._app
        app.child('Pause').point()
        time.sleep(2)
        app.child('Pause').click()

    def stop(self):
        app = self._app
        app.child('File').click()
        time.sleep(2)
        app.child('Quit').click()

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    lxmusic = Lxmusic(sunriver.linux)
    lxmusic.start()
    import IPython
    IPython.embed()
    lxmusic.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()


