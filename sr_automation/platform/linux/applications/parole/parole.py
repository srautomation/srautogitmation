import time
import os

class parole(object):
    def __init__(self, linux):
        self._linux = linux

    def start(self):
        self.linux_cmd = self._linux.cmd
        self._dogtail = self._linux.ui.dogtail
        self._process = self._dogtail.procedural.run('parole')
        time.sleep(3)
        self._app = self._dogtail.tree.root.application("parole")
        os.system('adb push /home/labuser/Videos/vids_h264/h264_gopro_running_dog.mp4 /data/debian/home/labuser/Videos')

    def stop(self):
        self.linux_cmd('kill %s'%self._process)
    
    def re_open(self):
        self.linux_cmd('parole')

    def open_media(self, movie):
        menuItem = self._app.menu('Media').menuItem('Open.')
        self._app.menu('Media').click()
        menuItem.click()
        self.dialog = self._app.dialog('Open Media Files')        
        self.dialog.child(name='Home').click()
        self.dialog.child(name='Videos').click()
        self.dialog.child(name='%s'%movie)
        self.dialog.button('Open').click()    

    def toggle_play_pause(self):
        app = self._app
        try:
            app.child(roleName = 'filler').click()
            app.child(name = 'Pause', roleName = 'push button').click()
        except:
            print 'did not pause'
        time.sleep(5)
        app.child(roleName = 'filler').click()
        try:
            app.child(name = 'Play', roleName = 'push button').click()
        except:
            print 'did not play'
        time.sleep(25)
