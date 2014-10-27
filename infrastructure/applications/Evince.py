import Application
import time

class Evince(Application._Editor):
    def __init__(self, linux):
        super(Evince, self).__init__(linux, 'evince')
    
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

