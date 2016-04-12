from sr_automation.platform.linux.applications.Settings.Settings_submenu import Settings_submenu
import time
import slash

class WallpaperAndScreenSaver(Settings_submenu):
    
    WALL_PAPAER_SUBMENU = (650, 200)
    WALLPAPER = "Wallpaper"
    SCREEN_SAVER = "Screen Saver"
    AUTO_LOCK = "Auto-Lock"
    START_AFTER = "Start After:"
    DURATION= {"minute": "1 Minute",
               "30 minutes": "30 Minutes",
               "None":"None"}
    AUTO_LOCK_COMBO_LABEL = "of inactivity."
    
    
    def __init__(self, settings):
        super(WallpaperAndScreenSaver, self).__init__(settings, self.WALL_PAPAER_SUBMENU)

    def enter_panel(self,panel):
        time.sleep(2)
        self._app.child(name=panel).grabFocus()
        self._app.child(name=panel).click()

    def change_screenSaver_Start_After(self,value):
        self.change_combobox_value(self.START_AFTER, value)
 
    def change_auto_lock_Start_After(self,value):
        self.change_combobox_value(self.AUTO_LOCK_COMBO_LABEL, value)
        
    def change_combobox_value(self,combo_label,combovalue):
        combo_box = self._app.child(name=combo_label).parent.parent.child(roleName="combo box")
        combo_box.click()
        time.sleep(1)
        combo_box_value = combo_box.child(name=combovalue)
        combo_box_value.click()
        
    def check_if_enabled(self):
        return self._app.child(name='Preview').sensitive

    def enable_disable_screenSaver(self):
        self._app.child(name='Preview').parent.parent.child(roleName='icon').click()
        
    def check_if_require_pass_when_waking_up(self):
        return  self._app.child(name='Preview').parent.parent.parent.parent.child(roleName='check box').isChecked
    
    def enable_disable_pass_when_waking_up(self):
        self._app.child(name='Preview').parent.parent.parent.parent.child(roleName='check box').click()
