from sr_automation.platform.linux.applications.dialogs.DialogOpen import DialogOpen
import time
from enum import Enum

class WriteMethod:
    String , Raw =range(2)

class Leafpad(object):
     
    def __init__(self, linux):
        self._linux = linux
        
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("leafpad")
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("leafpad")

    def stop(self):
        if self._process.is_running():
            self._process.terminate()

    def write_text(self, text,input_type=WriteMethod.String):
        app = self._app
        textBox = app.child(roleName = 'text')
        textBox.grabFocus()
        if input_type == WriteMethod.String :
            textBox.text = text
        elif input_type == WriteMethod.Raw :
            self._dogtail.rawinput.typeText(text)
    
    def read_text(self):
        app = self._app
        textBox = app.child(roleName = 'text')
        textBox.grabFocus()
        return textBox.text 

    def open(self, file):
        ''' file has to be in /root '''
        app = self._app
        textBox = app.child(roleName = 'text')
        textBox.grabFocus()
        app.child('File').click()
        time.sleep(1)
        app.child('Open...').click()
        time.sleep(1)
        save_changes = [i for i in app.findChildren(self._dogtail.predicate.GenericPredicate(roleName='label')) if i.name.startswith('Save changes to')]
        if save_changes: # dialog poped up
            app.child(name = 'No', roleName = 'push button').click()
        time.sleep(1)
        app.child('root').click()
        DialogOpen.open(app, file)

    def word_wrap(self):
        app = self._app
        app.child('Options').click()
        time.sleep(1)
        app.child('Word Wrap').click()

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    leafpad = Leafpad(sunriver.linux)
    leafpad.start()
    leafpad.open("/etc/sysctl.conf")
    raw_input("Press enter to finish")
    leafpad.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()

