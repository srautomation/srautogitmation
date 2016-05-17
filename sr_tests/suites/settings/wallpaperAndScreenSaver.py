import sr_tools.config as config
from sr_tests.suites.settings.settings_Base import SettingsBaseTest
import slash
from sr_automation.utils.ImageTools import ImageTools
from logbook import Logger

log = Logger("WALLPAPER_AND_SCREENSAVER")


class WallpaperAndScreenSaverTest(SettingsBaseTest):
    BEFORE_SNAPSHOT = "before_screensaver"
    SCREENSAVER_SNAPSHOT ="while_screensaver.png"
    AFTER_SNAPSHOT ="after_screensaver.png"
    SCREENSHOT_FILE = "screensaver.png"
    LOCK_FILE = "lock"
    
    def before(self):
        super(WallpaperAndScreenSaverTest, self).before()
        self.settings = slash.g.sunriver.settings 
        self.wallpaperAndScreenSaver = self.settings.wallpaperAndScreenSaver
        self.settings.start()
        self.wallpaperAndScreenSaver.enter()

    def test_screenSaver(self):
        log.info("test entering and exiting screensaver")
        self.configure_screensaver_and_lockscreen()
        ImageTools.snapShot_and_copy_file(self.BEFORE_SNAPSHOT)
        self.settings.dogtail.utils.doDelay(63)
        ImageTools.snapShot_and_copy_file(self.SCREENSAVER_SNAPSHOT)
        self.settings.dogtail.utils.doDelay(2)
        is_black_screen = ImageTools.check_if_black_screen( config.automation_files_dir +self.SCREENSAVER_SNAPSHOT)
        assert is_black_screen == False , "screensaver didn't work,black screen"
        s = ImageTools.compare_images(config.pictures_dir+self.SCREENSHOT_FILE, config.automation_files_dir +self.SCREENSAVER_SNAPSHOT)
        assert s > 0.8 , "screensaver didn't work"
        self.wake_up_screen()
        ImageTools.snapShot_and_copy_file(self.AFTER_SNAPSHOT)
        s = ImageTools.compare_images(config.automation_files_dir +self.AFTER_SNAPSHOT, config.automation_files_dir +self.BEFORE_SNAPSHOT)
        assert s > 0.9 , "didn't exit screensaver"
 
    def wake_up_screen(self):
        self.settings.dogtail.rawinput.keyCombo('<Shift><Shift>')
    
    def activate_screensaver(self,wanted_state):
        current_state = self.wallpaperAndScreenSaver.check_if_enabled()
        if wanted_state is not current_state:
            self.wallpaperAndScreenSaver.enable_disable_screenSaver()
    
    def dont_require_pass_after_screensaver(self):
        state = self.wallpaperAndScreenSaver.check_if_require_pass_when_waking_up()
        if state is True:
            self.wallpaperAndScreenSaver.enable_disable_pass_when_waking_up()
            
    def configure_screensaver_and_lockscreen(self):
        self.wallpaperAndScreenSaver.enter_panel(self.wallpaperAndScreenSaver.AUTO_LOCK)
        self.wallpaperAndScreenSaver.change_auto_lock_Start_After(self.wallpaperAndScreenSaver.DURATION["None"])
        self.wallpaperAndScreenSaver.enter_panel(self.wallpaperAndScreenSaver.SCREEN_SAVER)
        self.activate_screensaver(state.on)
        self.wallpaperAndScreenSaver.change_screenSaver_Start_After(self.wallpaperAndScreenSaver.DURATION["minute"])
        self.dont_require_pass_after_screensaver()
           
    def after(self):
        self.activate_screensaver(state.off)
        super(WallpaperAndScreenSaverTest, self).after()
        
class state():
    off = False
    on  = True

