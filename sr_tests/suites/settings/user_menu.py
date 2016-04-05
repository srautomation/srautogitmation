import sr_tools.config as config
from sr_tests.base.Base import BaseTest
from sr_automation.utils.ImageTools import ImageTools

from logbook import Logger
log = Logger("USER_MENU")

UserMenuTest_initialized =False
class UserMenuTest(BaseTest):
    
    USER_MENU_PICS = config.pictures_dir +"user_menu/"
    SETTINGS_PIC = USER_MENU_PICS + "user_menu_settings.png"
    LOCK_PIC = USER_MENU_PICS + "user_menu_lock.png"
    INSTALL_APPS_PIC = USER_MENU_PICS + "user_menu_installApps.png"
    SWITCH_TO_PHONE_PIC = USER_MENU_PICS + "user_menu_switchToPhone.png"
    HELP_PIC = USER_MENU_PICS + "user_menu_help.png"
    SYSTEM_INFO_PIC = USER_MENU_PICS + "user_menu_systemInfo.png"
    UPDATE_APPS_PIC = USER_MENU_PICS + "user_menu_UpdateApps.png"
    PRINTERS_PIC = USER_MENU_PICS + "user_menu_printers.png"
    RESTART_PIC = USER_MENU_PICS + "user_menu_restart.png"
 
    SNAPSHOT_USER_MENU = "user_menu_snapshot.png"
    COMBO = "<Ctrl><Shift>u"
    
    def before(self):
        global UserMenuTest_initialized
        if UserMenuTest_initialized is False:
            print "inside before"
            UserMenuTest_initialized = True
            super(UserMenuTest, self).before()
            self.dogtail.rawinput.keyCombo(self.COMBO)
            self.dogtail.utils.doDelay(1)
            ImageTools.snapShot_and_copy_file(self.SNAPSHOT_USER_MENU)
            
        
    def after(self):
        pass
    
    def test_settings_exist(self):
        self.check_submenu_exist(self.SETTINGS_PIC)
    
    def test_lock_exist(self):
        self.check_submenu_exist(self.LOCK_PIC)
    
    def test_printers_exist(self):
        self.check_submenu_exist(self.PRINTERS_PIC)
    
    def test_installApps_exist(self):
        self.check_submenu_exist(self.INSTALL_APPS_PIC)
    
    def test_updateApps_exist(self):
        self.check_submenu_exist(self.UPDATE_APPS_PIC)
    
    def test_systemInfo_exist(self):
        self.check_submenu_exist(self.SYSTEM_INFO_PIC)
    
    def test_help_exist(self):
        self.check_submenu_exist(self.HELP_PIC)
    
    def test_switchToPhone_exist(self):
        self.check_submenu_exist(self.SWITCH_TO_PHONE_PIC)
    
    def test_restart_exist(self):
        self.check_submenu_exist(self.RESTART_PIC)
    
    def check_submenu_exist(self,submenu): 
        submenu_name = str(submenu).rsplit('/',1)[1]
        log.info("check %s exists in user menu"%(submenu_name))
        stats = ImageTools.find_sub_image_in_image(self.SNAPSHOT_USER_MENU,submenu,needToSnap=False)
        print stats
        assert stats.max_value > 0.9 , "submenu %s wasn't in user menu" % (submenu_name)
           
