from tests.base.BaseTest import BaseTest
from tests.base.PerformanceBaseTest import PerformanceBaseTest
from infrastructure.applications import Leafpad, Evince, Firefox, Browser, Totem, Lxmusic, Gpicview, Pcmanfm
from infrastructure.applications.Libreoffice import Writer, Calc, Impress
import slash
import slash.log
import time
import IPython #TODO: use IPython insted of code
import code
import os
import subprocess

###############################################################################

RESULTS_PATH = os.environ['RESULTS_PATH']
RESOURCES_PATH = os.environ['RESOURCES_PATH']

TEST_PATH = os.path.dirname(os.path.realpath(__file__)) # Path of current file
RESULTS_PATH_LOCAL = os.path.join(TEST_PATH, 'results') # path of results inside the project
RESOURCES_PATH_LOCAL = os.path.join(TEST_PATH, 'resources')

RESOURCES_PATH_REMOTE = '/root' # Path of resources on DUT

###############################################################################

#TODO: fix session_start
'''
@slash.hooks.after_session_start.register # TODO: fix
def session_start():
    subprocess.Popen('adb push %s %s' % RESOURCES_PATH_LOCAL, RESOURCES_PATH_REMOTE,
            shell = True)

@slash.hooks.session_end.register
def session_end():
    for resource in os.listdir(RESOURCES_PATH_LOCAL):
        subprocess.Popen('adb shell rm %s' % os.path.join(RESOURCES_PATH_REMOTE,
            resource), shell = True)
'''

class BasicTests(PerformanceBaseTest):
    def before(self):
        super(BasicTests, self).before()
        # TODO: mv sym link creation to session_start
        subprocess.Popen('ln -s %s %s'  % (RESULTS_PATH, RESULTS_PATH_LOCAL), 
            shell = True)
        subprocess.Popen('ln -s %s %s'  % (RESOURCES_PATH, RESOURCES_PATH_LOCAL),
            shell = True)

    def after(self):
        super(BasicTests, self).after()
        # TODO: mv sym link deletion to session_end
        subprocess.Popen('rm %s' % RESULTS_PATH_LOCAL, shell = True)
        subprocess.Popen('rm %s' % RESOURCES_PATH_LOCAL, shell = True)
   
    def resource(self, name):
        return os.path.join(TEST_PATH, 'resources', name)

    def init_chromium(self):
        browser = Browser.Browser(self.linux)
        browser.start()
        return browser.chromium

    @PerformanceBaseTest.measure_entire_function
    def test_chromium_browse_text(self):
        chrome = self.init_chromium()
        chrome.get('http://www.theguardian.com')
        chrome.find_element_by_link_text('World').click()
        chrome.find_element_by_link_text('Middle East').click()
        time.sleep(7)
        chrome.find_element_by_link_text('Sport').click()
        chrome.find_element_by_link_text('Cricket').click()
#        code.interact(local=locals())
    
    @PerformanceBaseTest.measure_entire_function
    def test_chromium_stream_youtube(self):
        chrome = self.init_chromium()
        chrome.get('http://www.youtube.com/')
        search_text = chrome.find_element_by_id("masthead-search-term")
        search_text.click()
        search_text.send_keys("funny cats")
        chrome.find_element_by_id("search-btn").click()
        time.sleep(25)
        funny_cats_video = chrome.find_element_by_partial_link_text("Epic")
        funny_cats_video.click()
 

    @PerformanceBaseTest.measure_entire_function
    def test_writer_open_doc(self):
        writer = Writer.Writer(self.linux)
        writer.start()
        time.sleep(9)
        writer.open('Alice.odt')
        time.sleep(5)
        writer.set_bold()
        time.sleep(2)
        writer.set_italic()
        writer.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_calc_open_spreadsheet(self):
        calc = Calc.Calc(self.linux)
        calc.start('/root/DoctorWho.xlsx')
        time.sleep(9)
        calc.capitalize()
        calc.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_impress_start_presentation(self):
        impress = Impress.Impress(self.linux)
        impress.start()
        time.sleep(7)
        impress.open('humor-business.ppt')
        time.sleep(10)
        impress.start_slideshow(10)
        time.sleep(4)
        impress.stop()
    
    @PerformanceBaseTest.measure_entire_function
    def test_leafpad_open_file(self):
        leafpad = Leafpad.Leafpad(self.linux)
        leafpad.start()
        leafpad.write_text('lets open a text file')
        time.sleep(4)
        leafpad.open('example.txt')
        time.sleep(5)
        leafpad.stop()
    
    @PerformanceBaseTest.measure_entire_function
    def test_evince_open_pdf_save_as(self):
        evince = Evince.Evince(self.linux)
        evince.start()
        time.sleep(2)
        evince.open('example_pdf.pdf')
        time.sleep(3)
        evince.save_copy('myNewCopy')
        time.sleep(5)
        evince.stop()

    # TODO: fix
    @PerformanceBaseTest.measure_entire_function
    def test_firefox_open_cnn_then_world(self):
        firefox = Firefox.Firefox(self.linux)
        firefox.start()
        time.sleep(10)
        firefox.open('cnn.com')
        time.sleep(12)
        firefox.press_visible_link('World Sport')
        time.sleep(20)
        firefox.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_totem_play_movie(self):
        totem = Totem.Totem(self.linux)
        totem.start()
        time.sleep(9)
        totem.open('movie.avi')
        time.sleep(10)
        totem.toggle_play_pause()
        time.sleep(5)
        totem.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_lxmusic_play_music(self):
        lxmusic = Lxmusic.Lxmusic(self.linux)
        lxmusic.start()
        time.sleep(4)
        lxmusic.play('Silence')
        time.sleep(10)
        lxmusic.pause()
        time.sleep(3)
        lxmusic.play('vivaldi.mp3')
        time.sleep(10)
        lxmusic.pause()
        time.sleep(3)
        lxmusic.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_gpicview_browse_photos(self):
        gpicview = Gpicview.Gpicview(self.linux)
        gpicview.start()
        gpicview.open('image.jpg')
        time.sleep(4)
        gpicview.next_photo()
        time.sleep(4)
        gpicview.zoom_in()
        time.sleep(4)
        gpicview.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_pcmanfm_browse_dirs(self):
        pcmanfm = Pcmanfm.Pcmanfm(self.linux)
        pcmanfm.start()
        time.sleep(3)
        pcmanfm.goto('/etc/apt')
        time.sleep(5)
        pcmanfm.goto('/home/labuser')
        time.sleep(5)
        pcmanfm.stop()

    def thunderbird_compose():
        raise NotImplementedError

    def thunderbird_read_mail():
        raise NotImplementedError

    def dummy(self): # TODO: Erase
        code.interact(local = locals())

'''
    def _test(self):
        slash.log.set_log_color('my_logger', slash.logbook.NOTICE, "purple")
         
        tests = {   
                    self.leafpad_open_file : [],
                    self.evince_open_pdf_save_as : [],
                    self.firefox_open_cnn_then_world : [],
                    self.chromium_browse_text : [],
                    self.writer_open_doc : [],
                    self.calc_open_spreadsheet : [],
                    self.impress_start_presentation : [],
                    self.totem_play_movie : [],
                    self.lxmusic_play_music : [],
                    self.gpicview_browse_photos : []
                }
        
        for test in tests:
            slash.logger.notice('Starting test: %s ....' % test.__name__)
            self.generic_test(test, *tests[test])
'''
