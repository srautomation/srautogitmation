from sr_tests.suites.settings.settings_Base import SettingsBaseTest
import slash
from sr_automation.platform.linux.applications.Leafpad.Leafpad import Leafpad,WriteMethod
from sr_tools import config
from sr_automation.utils.ImageTools import ImageTools

from logbook import Logger
log = Logger("KEYBOARD")


class KeyboardBaseTest(SettingsBaseTest):

    def before(self):
        super(KeyboardBaseTest, self).before()
        self.settings = slash.g.sunriver.settings 
        self.keyboard = self.settings.language_and_keyboard
        self.settings.start()
        self.keyboard.enter()
        self.leafpad = Leafpad(slash.g.sunriver.linux)
        self.arabic=Language("arabic",config.pictures_dir + "Arabic.png",config.pictures_dir + "ArabicTopPanel.png")
        self.english=Language("English",config.pictures_dir +"English.png",config.pictures_dir + "EnglishTopPanel.png")
    

    def test_language_and_keyboard(self):
        self.keyboard.add_remove_keyboard_language()
        self.dogtail.utils.doDelay(5)
        self.checklanguage()

    def checklanguage(self):
        log.info("test adding another language(arabic) and writing in it ")
        text = "aba"
        text_in_arabic="شﻻش" 
        self.leafpad.start()
        self.change_language(self.english,self.arabic)
#         self.settings.dogtail.rawinput.keyCombo('<Shift><Alt_L>') 
#         self.dogtail.utils.doDelay(2)
        self.leafpad.write_text(text,WriteMethod.Raw) #write in arabic 
        print self.leafpad.read_text()
        assert self.leafpad.read_text() == text_in_arabic , "didn't wrote in arabic"
     
    def after(self): 
        self.leafpad.stop()
        self.change_language(self.arabic,self.english)
        self.keyboard.add_remove_keyboard_language()
        super(KeyboardBaseTest, self).after()

        
    def change_language(self,current_lang,desirable_lang):
        self.languge_panel_open(current_lang.top_panel_image)
        self.select_language(desirable_lang.menu_image)
        
    def languge_panel_open(self,IconPath):
        log.info("looking for language icon in top panel")
        Snapshot = "LangIcon.png"
        ImageTools.find_and_click_sub_image(Snapshot, IconPath)
        
    def select_language(self,lang_menu):
        Snapshot = "ChangeLang.png"
        ImageTools.find_and_click_sub_image(Snapshot, lang_menu)



class Language():
    
    def __init__(self,name,menu_image,top_panel_image):
        self.menu_image = menu_image
        self.name = name
        self.top_panel_image = top_panel_image
            
        
        
