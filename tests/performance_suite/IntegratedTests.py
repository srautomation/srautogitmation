import time, code, os

import slash

from tests.base.EmailBaseTest import EmailBaseTest
from tests.base.PerformanceBaseTest import PerformanceBaseTest
from tests.base.BrowserBaseTest import BrowserBaseTest
from infrastructure.applications import Browser, Evince, Gpicview, Leafpad,\
 Lxmusic, Pcmanfm, Thunderbird, Totem
from infrastructure.applications.Libreoffice import Calc, Impress, Writer

class IntegratedTests(PerformanceBaseTest, EmailBaseTest, BrowserBaseTest):
    def test_youtube_doc_pdf(self):
        DOC = 'Alice.odt'
        PDF = 'example_pdf.pdf' 
        self.prep_resource(DOC)
        self.prep_resource(PDF)
        chrome = self.init_chromium()
        chrome.get('http://www.youtube.com')
        search_text = chrome.find_element_by_id("masthead-search-term")
        search_text.click()
        search_text.send_keys("classical music")
        chrome.find_element_by_id("search-btn").click()
        time.sleep(25)
        vivaldi_video = chrome.find_element_by_partial_link_text("Vivaldi")
        vivaldi_video.click()
        time.sleep(90)
        writer = Writer.Writer(self.linux)
        writer.start()
        time.sleep(60)
        writer.open(DOC)
        time.sleep(30)
        writer.set_bold()
        time.sleep(10)
        evince = Evince.Evince(self.linux)
        evince.start()
        time.sleep(10)
        evince.open(PDF)
        time.sleep(5)
        writer.grab_focus('writer')
        time.sleep(2)
        writer.set_bold()

    def test_lxmusic_gpicview_calc(self):
        TRACK1 = 'vivaldi.mp3'
        TRACK2 = 'altj.mp3'
        PHOTO = 'image.jpg'
        SPREADSHEET = 'DoctorWho.xlsx'
        self.prep_resource(TRACK1)
        self.prep_resource(TRACK2)
        self.prep_resource(PHOTO)
        lxmusic = Lxmusic.Lxmusic(self.linux)
        lxmusic.start()
        time.sleep(5)
        lxmusic.play(TRACK1)
        time.sleep(10)
        gpicview = Gpicview.Gpicview(self.linux)
        gpicview.start()
        time.sleep(5)
        gpicview.open(PHOTO)
        time.sleep(5)
        for i in range(5):
            gpicview.next_photo()
            time.sleep(1)
        lxmusic.grab_focus()
        lxmusic.play(TRACK2)
        time.sleep(5)
        calc = Calc.Calc(self.linux)
        calc.start(os.path.join(slash.config.root.paths.resources_remote, SPREADSHEET))
        time.sleep(15)
        gpicview.grab_focus(PHOTO.split('.')[0])
        for i in range(5):
            gpicview.next_photo()
            time.sleep(1)
        calc.grab_focus()
        time.sleep(2)
        calc.capitalize()
        time.sleep(10)
        calc.stop()
        gpicview.stop()
        lxmusic.stop()

    def test_totem_thunderbird_leafpad(self):
        MOVIE = 'movie.avi'
        self.prep_resource(MOVIE)
        self.start_imapapp()
        thunderbird = Thunderbird.Thunderbird(self.linux)
        thunderbird.start()
        totem = Totem.Totem(self.linux)
        totem.start()
        totem.open(MOVIE)
        time.sleep(5)
        totem.toggle_play_pause()
        time.sleep(60)
        totem.toggle_play_pause()
        time.sleep(5)
        thunderbird.grab_focus('Thunderbird')
        composer = thunderbird.compose()
        time.sleep(5)
        composer.to('my@recepient.com')
        time.sleep(2)
        composer.subject('This is a subject')
        time.sleep(2)
        composer.body('This is a body')
        time.sleep(2)
        composer.save()
        time.sleep(2)
        leafpad = Leafpad.Leafpad(self.linux)
        leafpad.start()
        time.sleep(5)
        leafpad.write_text("I'm writing notes in my notepad")
        time.sleep(5)
        totem.grab_focus(MOVIE)
        totem.toggle_play_pause()
        time.sleep(60)
        totem.toggle_play_pause()
        leafpad.write_text("And maybe a few more notes...")
        time.sleep(5)
        leafpad.stop()
        totem.stop()
        thunderbird.stop()

    def test_chrome_news_radio_pcmanfm(self):
        chrome = self.init_chromium()
        time.sleep(20)
        chrome.get('http://sverigesradio.se/p2/')
        time.sleep(30)
        chrome.find_element_by_id('play-control').click()
        time.sleep(20)
        self.browser.new_tab()
        time.sleep(5)
        chrome.get('http://www.theguardian.com/uk')
        time.sleep(20)
        chrome.find_element_by_link_text('World').click()
        time.sleep(20)
        pcman = Pcmanfm.Pcmanfm(self.linux)
        pcman.start()
        time.sleep(5)
        pcman.goto('/home/labuser/Desktop')
        self.browser.grab_focus()
        time.sleep(2)
        self.browser.switch_tab(1)
        time.sleep(10)
        chrome.get('http://ntslive.co.uk/')
        time.sleep(15)
        self.browser.switch_tab(2)
        time.sleep(5)
        chrome.find_element_by_link_text('Middle East').click()
        time.sleep(20)
        self.browser.new_tab()
        time.sleep(5)
        chrome.get('http://en.wikipedia.org/wiki/Cougar')
        time.sleep(20)
        pcman.grab_focus('Desktop')
        pcman.goto('/usr/bin')
        time.sleep(10)
        self.browser.stop()

    def test_lxmusic_impress_thunderbird(self):
        TRACK = 'vivaldi.mp3'
        PRESENTATION = 'humor-business.ppt'
        self.prep_resource(TRACK)
        self.prep_resource(PRESENTATION)
        lxmusic = Lxmusic.Lxmusic(self.linux)
        lxmusic.start()
        time.sleep(10)
        lxmusic.play(TRACK)
        time.sleep(10)
        thunderbird = Thunderbird.Thunderbird(self.linux)
        thunderbird.start()
        time.sleep(10)
        thunderbird.search('bla bla bla')
        time.sleep(30)
        impress = Impress.Impress(self.linux)
        impress.start()
        time.sleep(15)
        impress.open(PRESENTATION)
        time.sleep(30)
        impress.start_slideshow(15)
        time.sleep(10)
        thunderbird.grab_focus('thunderbird')
        time.sleep(5)
        thunderbird.inbox()
        time.sleep(10)
        thunderbird.stop()
        impress.stop()
        lxmusic.stop()