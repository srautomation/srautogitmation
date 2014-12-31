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
import os
import subprocess
import IPython

class BasicTests(EmailBaseTest):
    def before(self):
        super(BasicTests, self).before()
        self.choose_email("intel.elad1@gmail.com").choose_folder("inbox").load()
        
    def after(self):
        super(BasicTests, self).after()

#    def test_interactive(self):
#        IPython.embed()
    
    def test_compare_subjects(self):
        result = self.compare_subject()
        slash.should.be(result, True)

    def test_compare_body(self):
        result = self.compare_body()
        slash.should.be(result, True)

    def test_compare_date(self):
        result = self.compare_date()
        slash.should.be(result, True)

    def test_compare_all(self):
        result = self.compare_all()
        slash.should.be(result, True)

