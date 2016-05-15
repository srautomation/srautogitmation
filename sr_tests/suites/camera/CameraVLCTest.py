import slash
from Base import CameraBaseTest
import time
from logbook import Logger
from termcolor import colored
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
        log.info('Testing recording and playing video')
        self.sunriver.vnc.OpenVnc()
        self.clean_recorded_folder()
        raw_input(colored('Press Enter to start recording:','green'))
        self.open_camera()
        time.sleep(4)
        if not self.androidUI(resourceId="com.android.camera2:id/shutter_button").exists:
            slash.add_error("Unable to open camera")
            slash.skip_test()
        time.sleep(2)
        self.record_by_duration(self.m_VideoDuration)
        time.sleep(5)
        video_dir = self.dogtail.procedural.os.listdir(self.m_VideoPath)
        assert len(video_dir) == 1 , "too many recorded videos"
        video_name = video_dir[0]
        self.play_video_in_device(video_name, self.m_VideoDuration)
        assert slash.g.sunriver.android.ui(text="Can't play this video.").exists == False , "Can not play video in device"
        try:
            self.play_video_in_vlc(video_name, self.m_VideoDuration)
        except TypeError:
            slash.add_error("Error in reading recorded file via VLC", 0)
        self.sunriver.vnc.CloseVnc()

    def test_big_buck_bunny(self):
        log.info("Testing Big Buck Bunny")
        try:
            slash.g.sunriver.linux.ui.dogtail.procedural.os.system('vlc --play-and-exit --fullscreen "/home/BigScreen/SDCard/mpeg4_big_buck_bunny_720p_surround.avi"')
        except:
            slash.add_error("Unable to play Big Buck Bunny in VLC")