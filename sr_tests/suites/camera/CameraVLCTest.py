import slash
from Base import CameraBaseTest
import time
from logbook import Logger
log = Logger("StressBaseInsideTest")

class CameraVLCTest(CameraBaseTest):

    @slash.hooks.session_start.register
    def start_video():
        log.info('starting camera test')

    def test_camera(self):
        if not self.check_vnc_open():
            slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Control>h')
        self.open_camera()
        self.start_stop_recording()
        time.sleep(15)
        self.start_stop_recording()
	self.open_vlc()
	 

