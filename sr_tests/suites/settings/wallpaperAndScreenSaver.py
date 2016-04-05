import sr_tools.config as config
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.utils.ImageTools import ImageTools
from logbook import Logger
import time

log = Logger("WALLPAPER_AND_SCREENSAVER")


class WallpaperAndScreenSaverTest(BaseTest):
    BEFORE_SNAPSHOT = "before_screensaver"
    SCREENSAVER_SNAPSHOT ="while_screensaver.png"
    AFTER_SNAPSHOT ="after_screensaver.png"
    SCREENSHOT_FILE = "screensaver.png"
    LOCK_FILE = "lock"
    initialized = False
    
    def before(self):
        if not self.initialized:
            self.initialized = True
            super(WallpaperAndScreenSaverTest, self).before()
            self.settings = Settings(slash.g.sunriver.linux)
            self.wallpaperAndScreenSaver = self.settings.wallpaperAndScreenSaver
        self.settings.start()
        self.wallpaperAndScreenSaver.enter()

    def test_screenSaver(self):
        log.info("test entering and exiting screensaver")
        self.wallpaperAndScreenSaver.enter_panel(self.wallpaperAndScreenSaver.SCREEN_SAVER)
        self.wallpaperAndScreenSaver.change_screenSaver_Start_After(self.wallpaperAndScreenSaver.DURATION["minute"])
        ImageTools.snapShot_and_copy_file(self.BEFORE_SNAPSHOT)
        self.settings.dogtail.utils.doDelay(63)
        ImageTools.snapShot_and_copy_file(self.SCREENSAVER_SNAPSHOT)
        time.sleep(2)
        is_black_screen = ImageTools.check_if_black_screen( config.automation_files_dir +self.SCREENSAVER_SNAPSHOT)
        assert is_black_screen == False , "screensaver didn't work,black screen"
        s = ImageTools.compare_images(config.pictures_dir+self.SCREENSHOT_FILE, config.automation_files_dir +self.SCREENSAVER_SNAPSHOT)
        assert s > 0.8 , "screensaver didn't work"
        self.wake_up_screen()
        ImageTools.snapShot_and_copy_file(self.AFTER_SNAPSHOT)
        s = ImageTools.compare_images(config.automation_files_dir +self.AFTER_SNAPSHOT, config.automation_files_dir +self.BEFORE_SNAPSHOT)
        assert s > 0.9 , "didn't exit screensaver"
        self.wallpaperAndScreenSaver.change_screenSaver_Start_After(self.wallpaperAndScreenSaver.DURATION["30 minutes"])
 
    def wake_up_screen(self):
        self.settings.dogtail.rawinput.keyCombo('<Shift><Shift>')
           
    def after(self):
        self.settings.stop()
