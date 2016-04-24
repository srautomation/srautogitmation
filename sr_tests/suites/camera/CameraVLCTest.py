import slash
from Base import CameraBaseTest
import time
from logbook import Logger
log = Logger("Camera and VLC")

class CameraVLCTest(CameraBaseTest):
    
    m_VideoDuration = 60
    m_VideoPath = "/home/BigScreen/Android/DCIM/Camera/"

    def clean_recorded_folder(self):
        log.info("Clearing past recordings")
        for vid_name in self.dogtail.procedural.os.listdir(self.m_VideoPath):
            path = self.dogtail.procedural.os.path.join(self.m_VideoPath, vid_name)
            self.dogtail.procedural.os.remove(path)
            
    def test_camera(self):
        self.sunriver.vnc.OpenVnc()
        self.clean_recorded_folder()
        self.open_camera()
        time.sleep(4)
        if not self.androidUI(resourceId="com.android.camera2:id/shutter_button").exists:
            slash.add_error("Unable to open camera")
            slash.skip_test()
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
        self.sunriver.vnc.CloseVnc()
