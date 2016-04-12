import time
from sr_automation.platform.linux.applications.Application import _Application

class Pcmanfm(_Application):
    
    APPName = 'pcmanfm'
    KILLAPP = 'killall %s'%APPName
    NewFileName = 'NewFile'
    NewFolderName = 'NewFolder'
    
    def __init__(self, linux):
        super(Pcmanfm, self).__init__(linux, start_cmd=self.APPName, stop_cmd=self.KILLAPP, dogtail_id=self.APPName)

#pcman doesnt recongnize created folder unless it is sorted to list view. list view button is not accessible throgh dogtail due to naming problem. currently written with rawinput which works only if window opens in exact place. when one day button name problem will be fixed - toggle sort func should be used in this test.

    def start_pcmanfm(self):
        self.start_dogtail_app(self.APPName)
        time.sleep(1)
        self._rawinput = self.dogtail.rawinput
    
    @property
    def Pcmanfm(self):
        return self.app

    def goto(self, dir_name):
        #self.toggle_sort()
        self.app.child(name=dir_name).doubleClick()
        time.sleep(1)

   # def toggle_sort(self):#need to sort to detail view in order to find folder using atspi
    #    tupxy = self.app.child(roleName='toggle button').click()
     #   print tupxy
      #  self._rawinput.click((int(tupxy[1]) + 42) , tupxy[1]) 
       # time.sleep(3)

    def new_folder(self, i_new_folder_name):
        self.app.child(name='New folder').click()
        time.sleep(1)
        self.app.child(roleName='dialog').child(roleName='text').text = i_new_folder_name
        self.app.child(roleName='dialog').child(name='OK').click()

    def new_file(self):
        self._rawinput.doubleClick(530, 215)
        self._rawinput.click(530, 215, button=3)
        self._rawinput.absoluteMotion(540, 230)
       #self.goto(self.NewFolderName)
        self._rawinput.click(button=3)
        self.app.child(name='Create New...').click()
        self.app.child(name='Folder').click()
        self.app.child(roleName='dialog').child(roleName='text').text = self.NewFileName
        self.app.child(roleName='dialog').child(name='OK').click()

    def drag_folder(self):
   #####self.toggle_sort()
   #####tupxy = self.app.child(name=self.NewFileName).position
   #####self.app.child(name=self.NewFileName).press()
   #####self._rawinput.press(530, 215)
   #####self._rawinput.absoluteMotion((int(tupxy[0])-160), (int(tupxy[1]) +200))
   #####self._rawinput.release((int(tupxy[0])-160), (int(tupxy[1])+200), button=2)
   #####self._rawinput.keyCombo('Enter')
   #####time.sleep(4)
   #####print 'Pressing on shortcut'
   #####self._rawinput.doubleClick((int(tupxy[0])-160), (int(tupxy[1]) +200))
   #####print 'Now Deleting user added folder'
   #####time.sleep(3)
   #####self._rawinput.click((int(tupxy[0])-160), (int(tupxy[1]) +200), button=3)
   #####self.app.child(name='Remove from Bookmarks').click()
        self._rawinput.press(530, 215)
        self._rawinput.absoluteMotion(370, 415)
        self._rawinput.release(370, 415, button=2)
        self._rawinput.keyCombo('Enter')
        time.sleep(4)
        print 'Pressing on shortcut'
        self._rawinput.doubleClick(370, 420)
        print 'Now Deleting user added folder'
        time.sleep(3)
        self._rawinput.click(370, 415, button=3)
        self._rawinput.click(520, 555)


    def breadCrumbs(self):
        print 'Clicking Previous Folder'
        time.sleep(2)
        self.app.child(name='Previous Folder').click()
        print 'Clicking Next Folder'
        time.sleep(2)
        self.app.child(name='Next Folder').click()

    def delete_folder(self, dir_name):
        self.goto(dir_name)
        self.app.child(name=self.NewFolderName).press()
        self._rawinput.keyCombo('Delete')
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


