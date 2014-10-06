# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from tests.base.BaseTest import BaseTest
from tests.base.PerformanceBaseTest import PerformanceBaseTest
from infrastructure.applications.Applications import Chromium, Leafpad, Evince, Firefox, Browser, Totem
from infrastructure.applications.Applications.Libreoffice import Writer, Calc, Impress
import slash
import slash.log
import time
import IPython #TODO: use IPython insted of code
import code
import os

class BasicTests(PerformanceBaseTest):
    def generic_test(self, test, *test_params):
        ''' runs a test and prints measurements '''
        with self.tester.timeit.measure():
            with self.device.resources.measure():
                    test(*test_params)
                    code.interact(local = locals())
                    time.sleep(5)
            
        mes = self.device.resources.measured
        slash.logger.notice("Finished generic test for %s" % test.func_name) 
        slash.logger.notice("============================================")
        slash.logger.notice("Test took: %f seconds to complete" % self.tester.timeit.measured)
        slash.logger.notice("Resources measurements results:")
        slash.logger.notice("cpu: AVG=%f, MAX=%f, MIN=%f" % (mes.cpu.avg, mes.cpu.max, mes.cpu.min))        
        slash.logger.notice("memory: AVG=%d, MAX=%d, MIN=%d" % (mes.mem.avg, mes.mem.max, mes.mem.min))
        slash.logger.notice("battery: AVG=%d, MAX=%d, MIN=%d" % (mes.bat.avg, mes.bat.max, mes.bat.min))

    def resource(self, name):
        return os.path.join(os.environ["PROJECT_ROOT"], "tests", "basic_suite", "resources", name) # TODO: use __file__

    def chromium_open_nytimes(self):
        self.chromium = Chromium.Chromium(self.linux)
        self.chromium.start('nytimes.com')
        time.sleep(7)

    def writer_open_doc(self):
        writer = Writer.Writer(self.linux)
        writer.start()
        time.sleep(9)
        writer.open('Alice.odt')
        time.sleep(5)
        writer.set_bold()
        time.sleep(2)
        writer.set_italic()
        writer.stop()

    def calc_open_spreadsheet(self):
        calc = Calc.Calc(self.linux)
        calc.start('/root/DoctorWho.xlsx')
        time.sleep(9)
        calc.capitalize()
        calc.stop()

    def impress_start_presentation(self):
        impress = Impress.Impress(self.linux)
        impress.start()
        time.sleep(7)
        impress.open('humor-business.ppt')
        time.sleep(10)
        impress.start_slideshow(10)
        time.sleep(4)
        impress.stop()

    def leafpad_open_file(self):
        self.leafpad = Leafpad.Leafpad(self.linux)
        self.leafpad.start()
        self.leafpad.write_text('lets open a text file')
        time.sleep(4)
        self.leafpad.open('example.txt')
        time.sleep(5)
        self.leafpad.stop()
    
    def evince_open_pdf_save_as(self):
        self.evince = Evince.Evince(self.linux)
        self.evince.start()
        time.sleep(2)
        self.evince.open('example_pdf.pdf')
        time.sleep(3)
        self.evince.save_copy('myNewCopy')
        time.sleep(5)
        self.evince.stop()

    def firefox_open_cnn_then_world(self):
        self.firefox = Firefox.Firefox(self.linux)
        self.firefox.start()
        time.sleep(10)
        self.firefox.open('cnn.com')
        time.sleep(12)
        self.firefox.press_visible_link('World Sport')
        time.sleep(20)
        self.firefox.stop()

    def selenium(self):
        self.linux.browser.start()
        self.linux.browser.go('cnn.com')

    def totem_play_movie(self):
        self.totem = Totem.Totem(self.linux)
        self.totem.start()
        time.sleep(9)
        self.totem.open('movie.avi')
        time.sleep(10)
        self.totem.toggle_play_pause()
        time.sleep(5)
        self.totem.stop()

    def dummy(self):
        pass

    def test(self):
        slash.log.set_log_color('my_logger', slash.logbook.NOTICE, "purple")
        '''
        tests = {   
                    self.leafpad_open_file : [],
                    self.evince_open_pdf_save_as : [],
                    self.firefox_open_cnn_then_world : [],
                    self.chromium_open_nytimes : [],
                    self.writer_open_doc : [],
                    self.calc_open_spreadsheet : [],
                    self.impress_start_presentation : [],
                    self.totem_play_movie : []
                }
        '''
        tests = { self.totem_play_movie : [] }
        
        for test in tests:
            slash.logger.notice('Starting test: %s ....' % test.__name__)
            self.generic_test(test)
