import time

class Evince(object):
    def __init__(self, linux):
        self._linux = linux
    
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("evince")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("evince")

    def stop(self):
        if self._process.is_running():
            self._process.terminate()
    
    def open(self, file):
        '''file has to be in /root '''
        app = self._app
        app.child('Document View').grabFocus()
        time.sleep(1)
        app.child('File').click()
        time.sleep(2)
        app.child('File').children[0].click()
        time.sleep(2)
        app.child(file).doubleClick()

    def save_copy(self, new_name):
        ''' new_name is w/o .pdf (i.e. only base name '''
        app = self._app
        app.child('Document View').grabFocus()
        time.sleep(1)
        app.child('File').click()
        time.sleep(2)
        if app.child('File').children[3].actions.has_key('click'):
            app.child('File').children[3].click()
            time.sleep(2)
            self._dogtail.config.config.load({'typingDelay': 0.15})
            self._dogtail.rawinput.typeText(new_name)
            app.child('Save').doubleClick()
            if app.isChild('Replace'):
                app.child('Replace').click()

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    evince = Evince(sunriver.linux)
    evince.start()
    import IPython
    IPython.embed()
    evince.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()



