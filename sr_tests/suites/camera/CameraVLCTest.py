import slash
from sr_automation.platform.sunriver.Sunriver import Sunriver
from Base import CameraBaseTest
import time
from logbook import Logger
log = Logger("Camera and VLC")

class CameraVLCTest(CameraBaseTest):
    
    m_VideoDuration = 60
    m_VideoPath = "/home/BigScreen/Android/DCIM/Camera/"

    def test_camera(self):
        slash.g.sunriver.vnc.OpenVnc()
        self.open_camera()
        self.record_by_duration(self.m_VideoDuration)
        video_dir = slash.g.sunriver.linux.ui.dogtail.procedural.os.listdir(self.m_VideoPath)
        slash.should.be(len(video_dir), 1)
        video_name = video_dir[0]
        self.play_video_in_device(video_name, self.m_VideoDuration)
        self.play_video_in_vlc(video_name, self.m_VideoDuration)
        slash.g.sunriver.linux.ui.dogtail.procedural.os.remove(self.m_VideoPath+video_name)
