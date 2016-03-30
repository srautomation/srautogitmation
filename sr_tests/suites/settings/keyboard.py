import time
from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Settings.Settings import Settings
from sr_automation.platform.linux.applications.Leafpad.Leafpad import *

from logbook import Logger
log = Logger("KEYBOARD")


class KeyboardBaseTest(BaseTest):
    
    initialized = False
    
    def before(self):
        if not self.initialized:
            self.initialized = True
            super(KeyboardBaseTest, self).before()
            self.settings = Settings(slash.g.sunriver.linux)
            self.keyboard = self.settings.language_and_keyboard
        self.settings.start()
        self.keyboard.enter()

    def test_language_and_keyboard(self):
        self.keyboard.add_remove_keyboard_language()
        time.sleep(5)
        self.checklanguage()
        self.keyboard.add_remove_keyboard_language()

    def checklanguage(self):
        text = "aba"
        text_in_arabic="شﻻش" 
        leafpad = Leafpad(slash.g.sunriver.linux)
        leafpad.start()
        self.settings.dogtail.rawinput.keyCombo('<Shift><Alt_L>') 
        leafpad.write_text(text,WriteMethod.Raw) #write in arabic 
        print leafpad.read_text()
        assert leafpad.read_text() == text_in_arabic
         
    def after(self):
        self.settings.stop()
