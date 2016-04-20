from sr_tests.suites.settings.settings_Base import SettingsBaseTest
import slash
from sr_automation.platform.linux.applications.Leafpad.Leafpad import Leafpad,WriteMethod

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


    def test_language_and_keyboard(self):
        self.keyboard.add_remove_keyboard_language()
        self.dogtail.utils.doDelay(5)
        self.checklanguage()
        self.keyboard.add_remove_keyboard_language()

    def checklanguage(self):
        log.info("test adding another language(arabic) and writing in it ")
        text = "aba"
        text_in_arabic="شﻻش" 
        self.leafpad.start()
        self.settings.dogtail.rawinput.keyCombo('<Shift><Alt_L>') 
        self.dogtail.utils.doDelay(2)
        self.leafpad.write_text(text,WriteMethod.Raw) #write in arabic 
        print self.leafpad.read_text()
        assert self.leafpad.read_text() == text_in_arabic , "didn't wrote in arabic"
     
    def after(self): 
        super(KeyboardBaseTest, self).after()
        self.leafpad.stop()
