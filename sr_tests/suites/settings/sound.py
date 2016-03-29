import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.utils.ImageTools import ImageTools

from logbook import Logger
log = Logger("SOUND")


class SoundBaseTest(BaseTest):
    SNAPSHOT_FULL_VOLUME="fullScreen-sound-full-volume.png"
    SNAPSHOT_MUTE = "fullScreen-sound-mute-volume.png"
    ICON_MUTE_PATH = "/tmp/automation-screenshots/sound-mute.png"
    ICON_FULL_VOLUME_PATH = "/tmp/automation-screenshots/sound-full-volume.png"
    initialized = False
    
    
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
    
    def check_volume_icon(self,image_name,subImage_path):
        boundries = self.find_crop_boundries()
        stats = ImageTools.find_sub_image_in_image(image_name, subImage_path, boundries)
        assert stats.max_value > 0.9 , "icon %s didn't work" % (image_name)  
        
    def find_crop_boundries(self):
        cmd="xdpyinfo | grep dimensions | awk '{print $2}' | cut -d 'x' -f1"
        image_width_string=slash.g.sunriver.linux.shell.runCommandWithReturnValue(cmd)
        image_width = int(image_width_string)
        crop_coordinates_dict = {
                             "y_min" : 0, 
                             "y_max" : 50,
                             "x_min" : 0,
                             "x_max" : image_width,   
                             "z_min": 0,
                             "z_max" : 3
                            }
        return crop_coordinates_dict