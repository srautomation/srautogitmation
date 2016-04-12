from sr_tests.suites.settings.settings_Base import SettingsBaseTest
from sr_tools import config
import slash
from sr_automation.utils.ImageTools import ImageTools
from logbook import Logger
log = Logger("SETTINGS_GUI")

UserMenuTest_initialized =False
class SettingsMenuTest(SettingsBaseTest):
 
    SETTINGS_MENU_PICS = config.pictures_dir +"settings_menu/"
    ACCOUNT_SUBMENU_PIC = SETTINGS_MENU_PICS + "account_menu.png"
    APPEARANCE_SUBMENU_PIC = SETTINGS_MENU_PICS + "appearance_menu.png"
    DISPLAY_SUBMENU_PIC = SETTINGS_MENU_PICS + "display_menu.png"
    LANGUAGE_SUBMENU_PIC = SETTINGS_MENU_PICS + "language_menu.png"
    SOUND_SUBMENU_PIC = SETTINGS_MENU_PICS + "sound_menu.png"
    WALLPAPER_SUBMENU_PIC = SETTINGS_MENU_PICS + "wallpaper_menu.png"

    SNAPSHOT_SETTINGS_MENU = "Settings_Menu.png"
    
    def before(self):
        global UserMenuTest_initialized
        if UserMenuTest_initialized is False :
            UserMenuTest_initialized = True
            super(SettingsBaseTest, self).before()
            self.settings = slash.g.sunriver.settings
            self.settings.start()
            self.dogtail.utils.doDelay(1)
            ImageTools.snapShot_and_copy_file(self.SNAPSHOT_SETTINGS_MENU)
            self.settings.stop()
    
    def after(self):
        pass
        
    def check_submenu_exist(self,submenu): 
        submenu_name = str(submenu).rsplit('/',1)[1].rsplit('.',1)[0]
        log.info("check %s exists in settings menu"%(submenu_name))
        stats = ImageTools.find_sub_image_in_image(self.SNAPSHOT_SETTINGS_MENU,submenu,needToSnap=False)
        print stats
        assert stats.max_value > 0.9 , "submenu %s wasn't in settings menu" % (submenu_name)
    
    def test_account_exist(self):
        self.check_submenu_exist(self.ACCOUNT_SUBMENU_PIC)
    
    def test_language_exist(self):
        self.check_submenu_exist(self.LANGUAGE_SUBMENU_PIC)
    
    def test_wallpaper_exist(self):
        self.check_submenu_exist(self.WALLPAPER_SUBMENU_PIC)
        
    def test_sound_exist(self):
        self.check_submenu_exist(self.SOUND_SUBMENU_PIC)
        
    def test_appearance(self):
        self.check_submenu_exist(self.APPEARANCE_SUBMENU_PIC)
        
    def test_display(self):
        self.check_submenu_exist(self.DISPLAY_SUBMENU_PIC)
           
    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)

    
if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    SettingsBaseTest = SettingsBaseTest(sunriver.linux)
    import IPython
    IPython.embed()