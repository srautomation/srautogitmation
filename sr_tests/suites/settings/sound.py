import cv2
import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.utils.ImageTools import ImageTools
from sr_automation.utils.TakeSnapshot import TakeSnapshot
from logbook import Logger
log = Logger("SOUND")


class SoundBaseTest(BaseTest):
    SNAPSHOT_PATH = "/tmp/"
    SNAPSHOT_FULL_VOLUME="fullScreen-sound-full-volume.png"
    SNAPSHOT_MUTE = "fullScreen-sound-mute-volume.png"
    ICON_MUTE_PATH = "/home/automation2/sr_automation/automation-screenshots/sound-mute.png"
    ICON_FULL_VOLUME_PATH = "/home/automation2/sr_automation/automation-screenshots/sound-full-volume.png"
    CHROOT_PATH = "/data/sunriver/fs/limited/"
    DIST_PATH = "/tmp/"
    initialized = False

    
    crop_coordinates_dict = {
                             "y_min" : 0, 
                             "y_max" : 50,
                             "x_min" : 0,
                             "x_max" : 1280, #TODO: use screen resolution width, not constant  
                             "z_min": 0,
                             "z_max" : 3
                            }
    
    def before(self):
        if not self.initialized:
            self.initialized = True
            super(SoundBaseTest, self).before()
            self.settings = Settings(slash.g.sunriver.linux)
            self.sound = self.settings.sound
        self.settings.start()
        self.sound.enter()
            
    def after(self):
        self.settings.stop()
    
    def test_sound_level_change(self):
        log.info("test- change volume through settings panel. check if the icon in the top panel updates accordingly")
        time.sleep(2)
        self.sound.change_output_volume_level(0)
        self.check_volume_icon(self.SNAPSHOT_MUTE,self.ICON_MUTE_PATH)
        time.sleep(2)
        self.sound.change_output_volume_level(100)
        self.check_volume_icon(self.SNAPSHOT_FULL_VOLUME,self.ICON_FULL_VOLUME_PATH)

    def check_volume_icon(self,image_name,path_subimage):
        snapshot = TakeSnapshot(self.settings.linux.shell)
        snapshot.take_snapshot(self.SNAPSHOT_PATH, image_name)
        ImageTools.copy_file_from_device(self.CHROOT_PATH+self.SNAPSHOT_PATH+image_name, self.DIST_PATH)
        time.sleep(2)
        image = cv2.imread(self.DIST_PATH + image_name)
        cropped_image = ImageTools.crop_image(image, self.crop_coordinates_dict)
        sub_image = cv2.imread(path_subimage)
        stats = ImageTools.find_sub_image_in_image(cropped_image, sub_image)
        log.info("best match percentage %f location (%f,%f)"% (stats.max_value,stats.max_location[0],stats.max_location[1]))
        assert stats.max_value > 0.9 , "icon %s didn't work" % (image_name)  