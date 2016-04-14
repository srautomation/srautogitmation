import slash
from Base import CameraBaseTest
import time
from logbook import Logger
log = Logger("Camera and VLC")

class CameraVLCTest(CameraBaseTest):
    
    m_VideoDuration = 60
    m_VideoPath = "/home/BigScreen/Android/DCIM/Camera/"

    def test_camera(self):
        self.sunriver.vnc.OpenVnc()
        time.sleep(2)
        self.open_camera()
        time.sleep(2)
        self.record_by_duration(self.m_VideoDuration)
        video_dir = self.dogtail.procedural.os.listdir(self.m_VideoPath)
        slash.should.be(len(video_dir), 1)
        video_name = video_dir[0]
        self.play_video_in_device(video_name, self.m_VideoDuration)
        try:
            self.play_video_in_vlc(video_name, self.m_VideoDuration)
        except TypeError:
            slash.add_error("Error in reading recorded file via VLC", 0)
        for vid_name in self.dogtail.procedural.os.listdir(self.m_VideoPath):
            path = self.dogtail.procedural.os.path.join(self.m_VideoPath, vid_name)
            self.dogtail.procedural.os.remove(path)
        self.sunriver.vnc.CloseVnc()
