from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
import time
from bunch import Bunch
import slash
import os

from logbook import Logger
log = Logger("Search and App Launcher")

class CameraBaseTest(BaseTest):
   
    def before(self):
        super(CameraBaseTest, self).before()
	
    def open_camera(self):
        log.info('Opening Camera')
        os.system("adb shell 'am start -a android.media.action.VIDEO_CAMERA'")

    def start_stop_recording(self):
    	log.info('Start/Stop Playing video')
        os.system("adb shell 'input keyevent 27'")

    def open_vlc(self):
        slash.g.sunriver.linux.ui.dogtail.procedural.os.system('vlc --fullscreen "/home/BigScreen/Android/DCIM/Camera/"&')
        time.sleep(15)
        for i in range(3):
            log.info('change volume')
            os.system("adb shell 'input keyevent 24'")
            time.sleep(3)
        for i in range(6):
            os.system("adb shell 'input keyevent 25'")
        slash.g.sunriver.stop()
        slash.g.sunriver.start()


    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
