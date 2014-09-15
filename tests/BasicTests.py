# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from infrastructure.BaseTest import BaseTest
from infrastructure.platform.linux.Applications import Chromium, Leafpad, Evince, Firefox, Browser
import slash
import slash.log
import time
import IPython #TODO: use IPython insted of code
import code

class BasicTests(BaseTest):
    def generic_test(self, test, *test_params):
        ''' runs a test and prints measurements '''
        with self.tester.timeout(1800000):
            with self.linux.resources.measure():
                    test(*test_params)
#                    code.interact(local = locals())
                    time.sleep(5)
            
            mes = self.linux.resources.measured
            slash.logger.notice("Finished generic test for %s" % test.func_name) 
            slash.logger.notice("============================================")
            slash.logger.notice("Resources measurements results:")
            slash.logger.notice("cpu: AVG=%f, MAX=%f, MIN=%f" % (mes.cpu.avg, mes.cpu.max, mes.cpu.min))        
            slash.logger.notice("memory: AVG=%d, MAX=%d, MIN=%d" % (mes.mem.avg, mes.mem.max, mes.mem.min))
            slash.logger.notice("battery: AVG=%d, MAX=%d, MIN=%d" % (mes.bat.avg, mes.bat.max, mes.bat.min))

    def chromium_open_nytimes(self):
        self.chromium = Chromium.Chromium(self.linux.cmd, self.linux.ui)
        self.chromium.start('nytimes.com')
        time.sleep(7)

    '''
    def writer_open_doc(self):
        writer = LibreOfficeWriter(self.linux.cmd, self.linux.ui)
        writer.start()
    '''

    def leafpad_open_file(self):
        self.leafpad = Leafpad.Leafpad(self.linux.cmd, self.linux.ui)
        self.leafpad.start()
        self.leafpad.write_text('lets open a text file')
        time.sleep(4)
        self.leafpad.open('example.txt')
        time.sleep(5)
        self.leafpad.stop()
    
    def evince_open_pdf_save_as(self):
        self.evince = Evince.Evince(self.linux.cmd, self.linux.ui)
        self.evince.start()
        time.sleep(2)
        self.evince.open('example_pdf.pdf')
        time.sleep(3)
        self.evince.save_copy('myNewCopy')
        time.sleep(5)
        self.evince.stop()

    def firefox_open_cnn_then_world(self):
        self.firefox = Firefox.Firefox(self.linux.cmd, self.linux.ui)
        self.firefox.start()
        time.sleep(10)
        self.firefox.open('cnn.com')
        time.sleep(12)
        self.firefox.press_visible_link('World Sport')
        time.sleep(20)
        self.firefox.stop()

    def firefox_open_youtube_and_search(self):
         pass 

    def selenium(self):
        self.linux.browser.start()
        self.linux.browser.go('cnn.com')
        #self.linux.browser

    def test(self):
        slash.log.set_log_color('my_logger', slash.logbook.NOTICE, "purple")
        
        tests = {   self.leafpad_open_file : [],
                    self.evince_open_pdf_save_as : [],
                    #self.firefox_open_cnn_then_world : [],
                    self.chromium_open_nytimes : [] }
        
        for test in tests:
            slash.logger.notice('Starting test: %s ....' % test.__name__)
            self.generic_test(test)
