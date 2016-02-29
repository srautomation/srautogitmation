import time

class Pcmanfm(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self):
        self._dogtail = self._linux.ui.dogtail
        self._linux.shell.os_system('killall pcmanfm')
        self._process = self._dogtail.procedural.run('pcmanfm')
        time.sleep(9)
        self.app = self._dogtail.tree.root.application('pcmanfm')

    @property
    def Pcmanfm(self):
        return self.app

    def stop(self):
        self._dogtail.procedural.run('kill pcmanfm')

    def goto(self, dir_name):
        self.app.child(name=dir_name).click()
        time.sleep(3)

    def new_folder(self):
        self.app.child(name='New folder').click()
        time.sleep(1)
        self.app.child(roleName='dialog').child(roleName='text').text = 'NewFolder'
        self.app.child(roleName='dialog').child(name='OK').click()

    def new_file(self):
        self._dogtail.rawinput.doubleClick(530, 215)
        self._dogtail.rawinput.click(530, 215, button=3)
        self._dogtail.rawinput.absoluteMotion(540, 230)
        self._dogtail.rawinput.click(900, 285, button=3)
        self.app.child(roleName='dialog').child(roleName='text').text = 'NewFile'
        self.app.child(roleName='dialog').child(name='OK').click()

    def drag_folder(self):
        self._dogtail.rawinput.press(530, 215)
        self._dogtail.rawinput.absoluteMotion(370, 415)
        self._dogtail.rawinput.release(370, 415, button=2)
        self._dogtail.rawinput.keyCombo('Enter')
        time.sleep(4)
        print 'Pressing on shortcut'
        self._dogtail.rawinput.doubleClick(370, 420)
        print 'Now Deleting user added folder'
        time.sleep(3)
        self._dogtail.rawinput.click(370, 415, button=3)
        self._dogtail.rawinput.click(520, 555)

    def breadCrumbs(self):
        print 'Clicking Previous Folder'
        time.sleep(2)
        self.app.child(name='Previous Folder').click()
        print 'Clicking Next Folder'
        time.sleep(2)
        self.app.child(name='Next Folder').click()

    def delete_folder(self, dir_name):
        self.goto(dir_name)
        self._dogtail.rawinput.press(530, 215)
        self._dogtail.rawinput.keyCombo('Delete')
        self.app.child(name='Question').child(name='Yes').doubleClick()


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


