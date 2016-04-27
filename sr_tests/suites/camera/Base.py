from sr_tests.base.Base import BaseTest
import time
import slash
import os

from logbook import Logger
log = Logger("Camera Test")

class CameraBaseTest(BaseTest):
   
    def before(self):
        super(CameraBaseTest, self).before()
        self.androidUI = self.sunriver.android.ui

    def open_camera(self):
        log.info('Opening Camera')
        os.system("adb shell 'am start -a android.media.action.VIDEO_CAMERA'")

    def record_by_duration(self, i_Duration):
        log.info('Recording Video')
        self.androidUI(resourceId="com.android.camera2:id/shutter_button").click()
        time.sleep(i_Duration)
        if self.androidUI(resourceId="com.android.camera2:id/recording_time").exists:
            self.androidUI(resourceId="com.android.camera2:id/shutter_button").click()
    
    @staticmethod
    def play_video_in_device(i_VideoName, i_Duration):
        log.info('Playing Video on Device')
        os.system("adb shell am start -n  com.android.gallery3d/.app.MovieActivity -d /storage/emulated/0/DCIM/Camera/"+i_VideoName)
        time.sleep(i_Duration)

    @staticmethod
    def play_video_in_vlc(i_VideoName, i_Duration):
        log.info('Playing Video in VLC')
        slash.g.sunriver.linux.ui.dogtail.procedural.os.system('vlc --play-and-exit --fullscreen "/home/BigScreen/Android/DCIM/Camera/'+i_VideoName)
        time.sleep(i_Duration)
