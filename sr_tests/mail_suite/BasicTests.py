from sr_tests.base.BaseTest import BaseTest
from sr_tests.base.PerformanceBaseTest import PerformanceBaseTest
from sr_tests.base.BrowserBaseTest import BrowserBaseTest
from sr_tests.base.EmailBaseTest import EmailBaseTest
from sr_automation.applications import Leafpad, Evince, Firefox, Browser, Totem,\
Lxmusic, Gpicview, Pcmanfm, Thunderbird
from sr_automation.applications.Libreoffice import Writer, Calc, Impress
import slash
import slash.log
import time
import IPython #TODO: use IPython insted of code
import code
import os
import subprocess

class BasicTests(EmailBaseTest):
    def before(self):
        self.browser = None
        super(BasicTests, self).before()
        
    def after(self):
        super(BasicTests, self).after()

    def test_comapre_subjects(self):
        code.interact(local = locals())

