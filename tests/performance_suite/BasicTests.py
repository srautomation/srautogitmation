from tests.base.BaseTest import BaseTest
from tests.base.PerformanceBaseTest import PerformanceBaseTest
from tests.base.BrowserBaseTest import BrowserBaseTest
from tests.base.EmailBaseTest import EmailBaseTest
from infrastructure.applications import Leafpad, Evince, Firefox, Browser, Totem,\
Lxmusic, Gpicview, Pcmanfm, Thunderbird
from infrastructure.applications.Libreoffice import Writer, Calc, Impress
import slash
import slash.log
import time
import IPython #TODO: use IPython insted of code
import code
import os
import subprocess

class BasicTests(PerformanceBaseTest, EmailBaseTest, BrowserBaseTest):
    def before(self):
        self.browser = None
        super(BasicTests, self).before()
        
    def after(self):
        super(BasicTests, self).after()

    @PerformanceBaseTest.measure_entire_function
    def test_chromium_browse_text(self):
        chrome = self.init_chromium()
        chrome.get('http://www.theguardian.com')
        chrome.find_element_by_link_text('World').click()
        chrome.find_element_by_link_text('Middle East').click()
        time.sleep(7)
        chrome.find_element_by_link_text('Sport').click()
        chrome.find_element_by_link_text('Cricket').click()
        time.sleep(20)
        self.browser.stop()
 
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
        time.sleep(30)
        self.browser.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_writer_open_doc(self):
        DOC = 'Alice.odt'
        self.prep_resource(DOC)
        writer = Writer.Writer(self.linux)
        writer.start()
        time.sleep(9)
        writer.open(DOC)
        time.sleep(5)
        writer.set_bold()
        time.sleep(2)
        writer.set_italic()
        time.sleep(20)
        writer.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_calc_open_spreadsheet(self):
        SPREADSHEET = 'DoctorWho.xlsx'
        self.prep_resource(SPREADSHEET)
        calc = Calc.Calc(self.linux)
        calc.start(os.path.join(slash.config.root.paths.resources_remote,
            SPREADSHEET))
        time.sleep(9)
        calc.capitalize()
        time.sleep(20)
        calc.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_impress_start_presentation(self):
        PRESENTATION = 'humor-business.ppt'
        self.prep_resource(PRESENTATION)
        impress = Impress.Impress(self.linux)
        impress.start()
        time.sleep(7)
        impress.open(PRESENTATION)
        time.sleep(10)
        impress.start_slideshow(10)
        time.sleep(4)
        time.sleep(20)
        impress.stop()
    
    @PerformanceBaseTest.measure_entire_function
    def test_leafpad_open_file(self):
        TXT = 'example.txt'
        self.prep_resource(TXT)
        leafpad = Leafpad.Leafpad(self.linux)
        leafpad.start()
        leafpad.write_text('lets open a text file')
        time.sleep(4)
        leafpad.open(TXT)
        time.sleep(5)
        leafpad.word_wrap()
        time.sleep(20)
        leafpad.stop()
    
    @PerformanceBaseTest.measure_entire_function
    def test_evince_open_pdf_save_as(self):
        PDF = 'example_pdf.pdf'
        self.prep_resource(PDF)
        evince = Evince.Evince(self.linux)
        evince.start()
        time.sleep(2)
        evince.open(PDF)
        time.sleep(3)
        evince.save_copy('myNewCopy')
        time.sleep(20)
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
        time.sleep(30)
        firefox.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_totem_play_movie(self):
        MOVIE = 'movie.avi'
        self.prep_resource(MOVIE)
        totem = Totem.Totem(self.linux)
        totem.start()
        time.sleep(9)
        totem.open(MOVIE)
        time.sleep(10)
        totem.toggle_play_pause()
        time.sleep(20)
        totem.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_lxmusic_play_music(self):
        TRACK = 'vivaldi.mp3'
        self.prep_resource(TRACK)
        lxmusic = Lxmusic.Lxmusic(self.linux)
        lxmusic.start()
        time.sleep(4)
        lxmusic.play('Silence')
        time.sleep(10)
        lxmusic.pause()
        time.sleep(3)
        lxmusic.play(TRACK)
        time.sleep(10)
        lxmusic.pause()
        time.sleep(20)
        lxmusic.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_gpicview_browse_photos(self):
        PHOTO = 'image.jpg'
        self.prep_resource(PHOTO)
        gpicview = Gpicview.Gpicview(self.linux)
        gpicview.start()
        gpicview.open(PHOTO)
        time.sleep(4)
        gpicview.next_photo()
        time.sleep(4)
        gpicview.zoom_in()
        time.sleep(20)
        gpicview.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_pcmanfm_browse_dirs(self):
        pcmanfm = Pcmanfm.Pcmanfm(self.linux)
        pcmanfm.start()
        time.sleep(3)
        pcmanfm.goto('/etc/apt')
        time.sleep(5)
        pcmanfm.goto('/home/labuser')
        time.sleep(20)
        pcmanfm.stop()

    @PerformanceBaseTest.measure_entire_function
    def test_thunderbird_compose(self):
        if not self.start_imapapp():
            slash.skip_test("Couldn't start ImapApp") 
        tb = Thunderbird.Thunderbird(self.linux)
        tb.start()
        time.sleep(5)
        composer = tb.compose()
        time.sleep(4)
        composer.to(('example@example.com',))
        time.sleep(3)
        composer.subject('This is a Subject')
        time.sleep(3)
        composer.body("This is the email's body")
        time.sleep(3)
        composer.save()
        time.sleep(20)
        tb.stop() 

    @PerformanceBaseTest.measure_entire_function
    def test_thunderbird_browse(self):
        if not self.start_imapapp():
            slash.skip_test("Couldn't start ImapApp") 
        tb = Thunderbird.Thunderbird(self.linux)
        tb.start()
        time.sleep(5)
        tb.drafts()
        time.sleep(3)
        tb.search('yoyoyo')
        time.sleep(3)
        tb.inbox()
        time.sleep(3)
        tb.trash()
        time.sleep(20)
        tb.stop()

    def dummy(self): # TODO: Erase
        code.interact(local = locals())