import sr_tools.config as config
from sr_tests.suites.settings.settings_Base import SettingsBaseTest
from sr_automation.utils.ImageTools import ImageTools
from sr_automation.platform.linux.applications.Leafpad.Leafpad import Leafpad,WriteMethod
import slash

from logbook import Logger
log = Logger("USER_MENU")

UserMenuTest_initialized =False
class UserMenuTest(SettingsBaseTest):
    
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
    
    LOCKSCREEN_PIC =USER_MENU_PICS + "lockscreen.png"
    TOP_PANEL_LOCKSCREEN=USER_MENU_PICS + "LockScreenTopPanel.png"
    
    SNAPSHOT_USER_MENU = "user_menu_snapshot.png"
    SNAPSHOT_AFTER_LOCK = "after_lock.png"
    SNAPSHOT_IN_LOCK = "in_lockscreen.png"
    SNAPSHOT_BEFORE_LOCK = "before_lock.png"
    
    
    MENU_BUTTON = (30,30)
    COMBO = "<Ctrl><Shift>u"
    
    def before(self):
        super(UserMenuTest, self).before()
        global UserMenuTest_initialized
        if UserMenuTest_initialized is False:
            UserMenuTest_initialized = True
            self.dogtail.rawinput.keyCombo(self.COMBO)
            ImageTools.snapShot_and_copy_file(self.SNAPSHOT_USER_MENU)
            self.dogtail.rawinput.click(self.MENU_BUTTON[0],self.MENU_BUTTON[1])
            
            
        
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
        submenu_name = str(submenu).rsplit('/',1)[1].rsplit('.',1)[0]
        log.info("check %s exists in user menu"%(submenu_name))
        stats = ImageTools.find_sub_image_in_image(self.SNAPSHOT_USER_MENU,submenu,needToSnap=False)
        print stats
        assert stats.max_value > 0.9 , "submenu %s wasn't in user menu" % (submenu_name)
    
    def click_at_submenu(self,submenu):
        self.dogtail.rawinput.click(self.MENU_BUTTON[0],self.MENU_BUTTON[1])
        stats = ImageTools.find_sub_image_in_image(self.SNAPSHOT_USER_MENU,submenu,needToSnap=False)
        self.dogtail.rawinput.click(stats.max_location[1],stats.max_location[0])
    
    def test_lock_screen_enter_and_exit(self):
        log.info("test entering and exiting lock screen")
        self.copy_current_pass()
        ImageTools.snapShot_and_copy_file(self.SNAPSHOT_BEFORE_LOCK)
        self.enter_lock_screen()
        ImageTools.snap_and_compare(self.SNAPSHOT_IN_LOCK, self.LOCKSCREEN_PIC, error="didn't enter lockscreen")
        self.check_top_panel_in_lockscreen()
        self.paste_pass_at_lockscreen()
        self.dogtail.utils.doDelay(1)
        ImageTools.snap_and_compare(self.SNAPSHOT_AFTER_LOCK,config.automation_files_dir+ self.SNAPSHOT_BEFORE_LOCK,error="didn't exit lock screen")
   
    def check_top_panel_in_lockscreen(self):
        log.info("check existence of the top panel in lock screen")
        stats = ImageTools.find_sub_image_in_image(self.SNAPSHOT_IN_LOCK, self.TOP_PANEL_LOCKSCREEN,needToSnap=False)
        assert stats.max_value > 0.9 , "Lockscreen has no Top Panel"
        
    def paste_pass_at_lockscreen(self):
        self.dogtail.rawinput.keyCombo('<Shift>') #exit screensaver
        self.dogtail.utils.doDelay(1)
        self.dogtail.rawinput.keyCombo('<Down>')
        self.dogtail.rawinput.keyCombo('<Ctrl>V')
        self.dogtail.rawinput.keyCombo('<Down>')
        self.dogtail.rawinput.keyCombo('<Enter>')
        
    def enter_lock_screen(self):
        self.click_at_submenu(self.LOCK_PIC)
        self.dogtail.utils.doDelay(8)
            
    def copy_current_pass(self):
        leafpad = Leafpad(slash.g.sunriver.linux)
        leafpad.start()
        leafpad.write_text(slash.g.sunriver.currentPass,WriteMethod.String)
        leafpad.copy_text()
        self.dogtail.utils.doDelay(1)        
        leafpad.stop()   
