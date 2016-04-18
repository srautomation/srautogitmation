from sr_tests.base.Base import BaseTest
import time
import slash
import os

from logbook import Logger
log = Logger("Camera Test")

class CameraBaseTest(BaseTest):
   
    def before(self):
        super(CameraBaseTest, self).before()

    def open_camera(self):
        log.info('Opening Camera')
        os.system("adb shell 'am start -a android.media.action.VIDEO_CAMERA'")

    def record_by_duration(self, i_Duration):
        log.info('Recording Video')
        os.system("adb shell 'input keyevent 27'")
        time.sleep(i_Duration)
        os.system("adb shell 'input keyevent 66'")
        os.system("adb shell 'input keyevent 66'")
    
    @staticmethod
    def play_video_in_device(i_VideoName, i_Duration):
        log.info('Playing Video on Device')
        os.system("adb shell am start -n  com.android.gallery3d/.app.MovieActivity -d /storage/emulated/0/DCIM/Camera/"+i_VideoName)
        time.sleep(i_Duration)

    @staticmethod
    def play_video_in_vlc(i_VideoName, i_Duration):
        log.info('Playing Video in VLC')
        slash.g.sunriver.linux.ui.dogtail.procedural.os.system('vlc --fullscreen "/home/BigScreen/Android/DCIM/Camera/'+i_VideoName)
        time.sleep(i_Duration)
