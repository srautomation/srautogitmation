from Application import _Application
import time

class Firefox(_Application):
    def __init__(self, linux):
        super(Firefox, self).__init__(linux, 'firefox', 'killall firefox')
            
    def start(self, url = ''):
        self._start_cmd = self._start_cmd + ' ' + url
        super(Firefox, self).start()
        is_window_visible = self._ldtp.waittillguiexist('Firefox')

    def open(self, url):
        app = self._dogtail.tree.root.application('Firefox')
        childs = app.findChildren(self._dogtail.predicate.GenericPredicate(name = 'Search or enter address', roleName = 'entry'))
        if len(childs) > 1: txt_box = 1
        else: txt_box = 0
        childs[txt_box].grabFocus()
        time.sleep(2)
        childs[txt_box].text = url
        time.sleep(2)
        self._dogtail.rawinput.pressKey('enter')

    def press_visible_link(self, link, retries = 10):
        app = self._dogtail.tree.root.application('Firefox')
        try:
            childs = app.findChildren(self._dogtail.predicate.GenericPredicate(name = 'Search or enter address', 
                                                                                roleName = 'entry'))
            if len(childs) > 1: txt_box = 1
            else: txt_box = 0
            #childs[txt_box].grabFocus()
        except TypeError:
            pass
        time.sleep(2)
        counter = 0
        while not app.isChild(link) and counter < retries:
            time.sleep(4)
            counter += 1
        app.child(link).click()
