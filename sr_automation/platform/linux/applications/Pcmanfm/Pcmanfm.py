import time

class Pcmanfm(object):
    def __init__(self, linux):
        self._linux = linux
    
    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._process = self._dogtail.procedural.run('pcmanfm')
        time.sleep(9)
        self._app = self._dogtail.tree.root.application('pcmanfm')
 
    def stop(self):
        self.linux_cmd('kill %s'%self._process)

    def goto(self, dir):
        app = self._app
        app.child(roleName = 'text').text = dir
        time.sleep(3)
        app.child('Jump to').click()

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    pcmanfm = Pcmanfm(sunriver.linux)
    pcmanfm.start()
    pcmanfm.goto("/root")
    import IPython
    IPython.embed()
    pcmanfm.stop()

    sunriver.stop()


