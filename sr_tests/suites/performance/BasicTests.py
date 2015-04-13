from sr_tests.suites.performance.Base import PerformanceBaseTest
from sr_automation.platform.linux.applications.Leafpad.Leafpad         import Leafpad
from sr_automation.platform.linux.applications.Evince.Evince           import Evince
from sr_automation.platform.linux.applications.Firefox.Firefox         import Firefox
from sr_automation.platform.linux.applications.Browser.Browser         import Browser
from sr_automation.platform.linux.applications.Totem.Totem             import Totem
from sr_automation.platform.linux.applications.Lxmusic.Lxmusic         import Lxmusic
from sr_automation.platform.linux.applications.Gpicview.Gpicview       import Gpicview
from sr_automation.platform.linux.applications.Pcmanfm.Pcmanfm         import Pcmanfm
from sr_automation.platform.linux.applications.Thunderbird.Thunderbird import Thunderbird
from sr_automation.platform.linux.applications.Skype.Skype             import Skype
from sr_automation.platform.linux.applications.Libreoffice.Writer.Writer   import Writer
from sr_automation.platform.linux.applications.Libreoffice.Calc.Calc       import Calc
from sr_automation.platform.linux.applications.Libreoffice.Impress.Impress import Impress

import slash
import time
import os

class BasicTests(PerformanceBaseTest):
    def test_chromium_browse_text(self):
        with self.measure():
            chrome = self.init_chromium()
            chrome.get('http://www.theguardian.com')
            chrome.find_element_by_link_text('World').click()
            chrome.find_element_by_link_text('Middle East').click()
            time.sleep(7)
            chrome.find_element_by_link_text('Sport').click()
            chrome.find_element_by_link_text('Cricket').click()
            time.sleep(20)
            self.browser.stop()
 
    def test_chromium_stream_youtube(self):
        with self.measure():
            chrome = self.init_chromium()
            chrome.get('http://www.youtube.com/')
            search_text = chrome.find_element_by_id("masthead-search-term")
            search_text.click()
            search_text.send_keys("funny cats")
            search_btn = chrome.find_element_by_id("search-btn")
            try:
                search_btn.click()
            except Browser.exceptions.WebDriverException as e:
                try: # try dismissing new youtube popup
                    chrome.find_element_by_class_name('iph-dialog-dismiss-container').click()
                except:
                    time.sleep(10) # hacky- wait for popup to fade
                search_btn.click()
            time.sleep(25)
            funny_cats_video = chrome.find_element_by_partial_link_text("Epic")
            funny_cats_video.click()
            time.sleep(30)
            self.browser.stop()

    def test_writer_open_doc(self):
        with self.measure():
            writer = Writer.Writer(self.linux)
            writer.start()
            time.sleep(9)
            writer.open(self.config.sr.files.docx)
            time.sleep(5)
            writer.set_bold()
            time.sleep(2)
            writer.set_italic()
            time.sleep(20)
            writer.stop()

    def test_calc_open_spreadsheet(self):
        with self.measure():
            calc = Calc.Calc(self.linux)
            calc.start(self.resources.path(self.config.sr.files.xlsx))
            time.sleep(9)
            calc.capitalize()
            time.sleep(20)
            calc.stop()

    def test_impress_start_presentation(self):
        with self.measure():
            impress = Impress.Impress(self.linux)
            impress.start()
            time.sleep(7)
            impress.open(self.config.sr.files.ppt)
            time.sleep(10)
            impress.start_slideshow(10)
            time.sleep(4)
            time.sleep(20)
            impress.stop()
    
    def test_leafpad_open_file(self):
        with self.measure():
            leafpad = Leafpad.Leafpad(self.linux)
            leafpad.start()
            leafpad.write_text('lets open a text file')
            time.sleep(4)
            leafpad.open(self.config.sr.files.txt)
            time.sleep(5)
            leafpad.word_wrap()
            time.sleep(20)
            leafpad.stop()
    
    def test_evince_open_pdf_save_as(self):
        with self.measure():
            evince = Evince.Evince(self.linux)
            evince.start()
            time.sleep(2)
            evince.open(self.config.sr.files.pdf)
            time.sleep(3)
            evince.save_copy('myNewCopy')
            time.sleep(20)
            evince.stop()

    # TODO: fix
    def test_firefox_open_cnn_then_world(self):
        with self.measure():
            firefox = Firefox.Firefox(self.linux)
            firefox.start()
            time.sleep(10)
            firefox.open('cnn.com')
            time.sleep(12)
            firefox.press_visible_link('World Sport')
            time.sleep(30)
            firefox.stop()

    def test_totem_play_movie(self):
        with self.measure():
            totem = Totem.Totem(self.linux)
            totem.start()
            time.sleep(9)
            totem.open(self.config.sr.files.avi)
            time.sleep(10)
            totem.toggle_play_pause()
            time.sleep(20)
            totem.stop()

    def test_lxmusic_play_music(self):
        with self.measure():
            lxmusic = Lxmusic.Lxmusic(self.linux)
            lxmusic.start()
            time.sleep(4)
            lxmusic.play('Silence')
            time.sleep(10)
            lxmusic.pause()
            time.sleep(3)
            lxmusic.play(self.config.sr.files.mp3)
            time.sleep(10)
            lxmusic.pause()
            time.sleep(20)
            lxmusic.stop()

    def test_gpicview_browse_photos(self):
        with self.measure():
            gpicview = Gpicview.Gpicview(self.linux)
            gpicview.start()
            gpicview.open(self.config.sr.jpg)
            time.sleep(4)
            gpicview.next_photo()
            time.sleep(4)
            gpicview.zoom_in()
            time.sleep(20)
            gpicview.stop()

    def test_pcmanfm_browse_dirs(self):
        with self.measure():
            pcmanfm = Pcmanfm.Pcmanfm(self.linux)
            pcmanfm.start()
            time.sleep(3)
            pcmanfm.goto('/etc/apt')
            time.sleep(5)
            pcmanfm.goto('/home/labuser')
            time.sleep(20)
            pcmanfm.stop()

    def test_thunderbird_compose(self):
        with self.measure():
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

    def test_thunderbird_browse(self):
        with self.measure():
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

    def test_skype(self):
        ''' 
        NOT TESTED! 
        Initiates a call to Skype's echo service and inject a wav file as input. 
        '''
        with self.measure():
            WAV = 'alt-j.wav'
            self.prep_resource(WAV)
            skype = Skype.Skype(self.linux)
            skype.start()
            skype.input_device = Skype.Skype.INPUT_DEVICE_TYPE_FILE, WAV
            call = skype.place_call('echo123')
            # wait for call to finish, TODO: check end cases
            while call.Status != skype._Skype4Py.clsFinished:
                time.sleep(1)
