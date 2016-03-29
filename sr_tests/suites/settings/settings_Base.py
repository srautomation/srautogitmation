import time
import crypt
import cv2
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.platform.linux.applications.Leafpad.Leafpad import *
from sr_automation.utils.ImageTools import ImageTools
from sr_automation.utils.TakeSnapshot import TakeSnapshot
from sr_tests.suites.settings.account import AccountBaseTest
from logbook import Logger
log = Logger("SETTINGS")

class SettingsBaseTest(BaseTest):
    PRIVILAGE_USER="BigScreen"
    NEW_USER = "test_user1"
    OLD_PASS = "123qwezxc"#TODO how do we get the old password?
    NEW_PASS = "1@password"
    LANGUGE_CHECK = "قخمخق"
    VERIFY_PASS = NEW_PASS
    HINT = "1@password"
    pass_entries = [OLD_PASS, NEW_PASS, VERIFY_PASS, HINT]
    initialized = False
    SNAPSHOT_PATH = "/tmp/"
    SNAPSHOT_FULL_VOLUME="fullScreen-sound-full-volume.png"
    SNAPSHOT_MUTE = "fullScreen-sound-mute-volume.png"
    ICON_MUTE_PATH = "/home/automation2/sr_automation/automation-screenshots/sound-mute.png"
    ICON_FULL_VOLUME_PATH = "/home/automation2/sr_automation/automation-screenshots/sound-full-volume.png"
    CHROOT_PATH = "/data/sunriver/fs/limited/"
    DIST_PATH = "/tmp/"
    
    crop_coordinates_dict = {
                             "y_min" : 0, 
                             "y_max" : 50,
                             "x_min" : 0,
                             "x_max" : 1280, #TODO: use screen resolution width, not constant  
                             "z_min": 0,
                             "z_max" : 3
                            }
    
    def before(self):
        if not self.initialized :
            super(SettingsBaseTest, self).before()
            SettingsBaseTest.start_settings()
            self.initialized = True 
    
    def test_account(self):
        self.Account_test = AccountBaseTest()
            
    @staticmethod
    def start_settings():
        slash.g.settings = Settings(slash.g.sunriver.linux)
        slash.g.settings.start()
    
    #---------------------------------------- def test_sound_level_change(self):
        #---------------------------------------- slash.g.settings.sound.enter()
        #--------------------------------------------------------- time.sleep(2)
        #------------------ slash.g.settings.sound.change_output_volume_level(0)
        #-------- self.check_volume_icon(self.SNAPSHOT_MUTE,self.ICON_MUTE_PATH)
        #--------------------------------------------------------- time.sleep(2)
        #---------------- slash.g.settings.sound.change_output_volume_level(100)
        # self.check_volume_icon(self.SNAPSHOT_FULL_VOLUME,self.ICON_FULL_VOLUME_PATH)
        #----------------------------------------- slash.g.settings.sound.exit()

    def check_volume_icon(self,image_name,path_subimage):
        snapshot = TakeSnapshot(slash.g.settings._linux.shell)
        snapshot.take_snapshot(self.SNAPSHOT_PATH, image_name)
        ImageTools.copy_file_from_device(self.CHROOT_PATH+self.SNAPSHOT_PATH+image_name, self.DIST_PATH)
        time.sleep(2)
        image = cv2.imread(self.DIST_PATH + image_name)
        cropped_image = ImageTools.crop_image(image, self.crop_coordinates_dict)
        sub_image = cv2.imread(path_subimage)
        stats = ImageTools.find_sub_image_in_image(cropped_image, sub_image)
        log.info("stats %f (%f,%f)"% (stats.max_value,stats.max_location[0],stats.max_location[1]))
        assert stats.max_value > 0.9 , "icon %s didn't work" % (image_name)   
            
    #---------------------------------------- def test_account_changeUser(self):
        #-------------------------------------- slash.g.settings.account.enter()
        #------------------ slash.g.settings.account.set_username(self.NEW_USER)
        #------- assert slash.g.settings.account.get_username() == self.NEW_USER
        #--------------------------------------- slash.g.settings.account.exit()


    #---------------------------------------- def test_account_changePass(self):
        #-------------------------------------- slash.g.settings.account.enter()
        #--------------- slash.g.settings.account.change_pass(self.pass_entries)
        #-------------------------------------------------- self.checkPassword()
        #--------------------------------------- slash.g.settings.account.exit()
         
    def checkPassword(self):
        time.sleep(2)
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = slash.g.settings._linux.shell.runCommandWithReturnValue(cmd)
        assert crypt.crypt(self.NEW_PASS,output) == output
    
    
    #------------------------------------- def test_language_and_keyboard(self):
        #------------------------ slash.g.settings.language_and_keyboard.enter()
        #- slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        #--------------------------------------------------------- time.sleep(5)
        #-------------------------------------------------- self.checklanguage()
        #- slash.g.settings.language_and_keyboard.add_remove_keyboard_language()
        #------------------------- slash.g.settings.language_and_keyboard.exit()

    def checklanguage(self):
        text = "aba"
        text_in_arabic="شﻻش" 
        leafpad = Leafpad(slash.g.sunriver.linux)
        leafpad.start()
        slash.g.settings.dogtail.rawinput.keyCombo('<Shift><Alt_L>') 
        leafpad.write_text(text,WriteMethod.Raw) #write in arabic 
        print leafpad.read_text()
        assert leafpad.read_text() == text_in_arabic
 
    def after(self):
        time.sleep(3)
        slash.g.settings.return_from_submenu()
        

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)


if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    SettingsBaseTest = SettingsBaseTest(sunriver.linux)
    import IPython
    IPython.embed()
   