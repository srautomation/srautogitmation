import time

class Firefox(object):
    def __init__(self, linux):
        self._linux = linux
            
    def start(self, url=""):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._linux.cmd("firefox {}".format(url))
        time.sleep(9)
        self._app = self._dogtail.tree.root.application("Firefox")
        #is_window_visible = self._ldtp.waittillguiexist('Firefox')

    def stop(self):
        if self._process.is_running():
            self._linux.cmd("killall firefox")
        if self._process.is_running():
            self._process.terminate()
    
    def open(self, url):
        app = self._app
        childs = app.findChildren(self._dogtail.predicate.GenericPredicate(name = 'Search or enter address', roleName = 'entry'))
        if len(childs) > 1: txt_box = 1
        else: txt_box = 0
        childs[txt_box].grabFocus()
        time.sleep(2)
        childs[txt_box].text = url
        time.sleep(2)
        self._dogtail.rawinput.pressKey('enter')

    def press_visible_link(self, link, retries = 10):
        app = self._app
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

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    
    firefox = Firefox(sunriver.linux)
    firefox.start("www.youtube.com")
    import IPython
    IPython.embed()
    firefox.stop()

    sunriver.linux.stop()
    sunriver.desktop.stop()




