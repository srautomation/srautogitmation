import Application
import time

class Leafpad(Application._Editor):
    def __init__(self, cmd, ui):
        super(Leafpad, self).__init__(cmd, ui, 'leafpad', 'leafpad')

    def write_text(self, text):
        app = self._dogtail.tree.root.application('leafpad')
        textBox = app.child(roleName = 'text')
        textBox.grabFocus()
        textBox.text = text

    def open(self, file):
        ''' file has to be in /root '''
        app = self._dogtail.tree.root.application('leafpad')
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
        time.sleep(5)
        app.child(file).doubleClick()
        time.sleep(4)
        app.child('Options').click()
        time.sleep(1)
        app.child('Word Wrap').click()
