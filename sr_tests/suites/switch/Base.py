from sr_tests.base.Base import BaseTest
from sr_automation.utils.IMGCompare import IMGCompare
import slash
import slash.log
import time
import os
import subprocess

class SwitchBaseTest(BaseTest):

    times_to_switch = 500

    #def test_many_switches(self):
     #   for i in range(self.times_to_switch):
      #      slash.logger.info('Cycle #%s' % (i+1))
      #      slash.g.sunriver.switch_to_android.switch()
      #      slash.should.be(self.sunriver.desktop.is_desktop_running(), False)
      #      slash.g.sunriver.desktop.switch_to_desktop()
      #      slash.should.be(self.sunriver.desktop.is_desktop_running(), True)
    

    def test_image_comparison(self):
        img = IMGCompare()
        success_holder = 0
        for i in range(self.times_to_switch):
            slash.logger.info('Cycle #%s' % (i+1))
            slash.g.sunriver.switch_to_android.switch()
            time.sleep(4)
            slash.should.be(self.sunriver.desktop.is_desktop_running(), False)
            slash.g.sunriver.desktop.switch_to_desktop()
            time.sleep(4)
	    slash.should.be(self.sunriver.desktop.is_desktop_running(), True)
            #slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>l')
           # time.sleep(5)
           #slash.g.sunriver.linux.ui.dogtail.utils.screenshot('AppLauncherOnPhone.png', False)
           # time.sleep(5)
            #os.system('sudo adb pull /data/debian/tmp/dogtail-labuser/AppLauncherOnPhone.png /home/labuser/sr_automation/automation-screenshots/ApplauncherOnPhone.png')
           # if img.image_compare('/home/labuser/sr_automation/automation-screenshots/AppLauncher.png', '/home/labuser/sr_automation/automation-screenshots/ApplauncherOnPhone.png'):
               # print True 
               # success_holder +=1
           # slash.g.sunriver.linux.cmd('rm /tmp/dogtail-labuser/SearchOnPhone.png')
           # os.system('sudo rm /home/labuser/sr_automation/automation-screenshots/SearchOnPhone.png')
       # slash.should.be(self.times_to_switch , success_holder)      
