import Application
import time

class Leafpad(Application._Editor):
    def __init__(self, linux):
        super(Leafpad, self).__init__(linux, 'leafpad')

    def write_text(self, text):
        app = self._app
        textBox = app.child(roleName = 'text')
        textBox.grabFocus()
        textBox.text = text

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
        self._open(file)

    def word_wrap(self):
        app = self._app
        app.child('Options').click()
        time.sleep(1)
        app.child('Word Wrap').click()
