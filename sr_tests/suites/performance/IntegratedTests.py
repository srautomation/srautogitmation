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

class IntegratedTests(PerformanceBaseTest):
    def test_youtube_doc_pdf(self):
        with self.measure():
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
            writer.open(self.config.sr.files.odt)
            time.sleep(30)
            writer.set_bold()
            time.sleep(10)
            evince = Evince.Evince(self.linux)
            evince.start()
            time.sleep(10)
            evince.open(self.config.sr.files.pdf)
            time.sleep(5)
            writer.grab_focus('writer')
            time.sleep(2)
            writer.set_bold()

    def test_lxmusic_gpicview_calc(self):
        with self.measure():
            lxmusic = Lxmusic.Lxmusic(self.linux)
            lxmusic.start()
            time.sleep(5)
            lxmusic.play(self.config.sr.files.track1)
            time.sleep(10)
            gpicview = Gpicview.Gpicview(self.linux)
            gpicview.start()
            time.sleep(5)
            gpicview.open(self.config.sr.files.jpg)
            time.sleep(5)
            for i in range(5):
                gpicview.next_photo()
                time.sleep(1)
            lxmusic.grab_focus()
            lxmusic.play(self.config.sr.files.track2)
            time.sleep(5)
            calc = Calc.Calc(self.linux)
            calc.start(self.resources.path(self.config.sr.files.xlsx))
            time.sleep(15)
            gpicview.grab_focus(self.config.sr.files.jpg.split('.')[0])
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
        with self.measure():
            self.start_imapapp()
            thunderbird = Thunderbird.Thunderbird(self.linux)
            thunderbird.start()
            totem = Totem.Totem(self.linux)
            totem.start()
            totem.open(self.config.sr.files.avi)
            time.sleep(5)
            totem.toggle_play_pause()
            time.sleep(60)
            totem.toggle_play_pause()
            time.sleep(5)
            thunderbird.grab_focus('Thunderbird')
            composer = thunderbird.compose()
            time.sleep(5)
            composer.to(['my@recepient.com'])
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
            totem.grab_focus(self.config.sr.files.avi)
            totem.toggle_play_pause()
            time.sleep(60)
            totem.toggle_play_pause()
            leafpad.write_text("And maybe a few more notes...")
            time.sleep(5)
            leafpad.stop()
            totem.stop()
            thunderbird.stop()

    def test_chrome_news_radio_pcmanfm(self):
        with self.measure():
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
        with self.measure():
            lxmusic = Lxmusic.Lxmusic(self.linux)
            lxmusic.start()
            time.sleep(10)
            lxmusic.play(self.config.sr.files.mp3)
            time.sleep(10)
            thunderbird = Thunderbird.Thunderbird(self.linux)
            thunderbird.start()
            time.sleep(10)
            thunderbird.search('bla bla bla')
            time.sleep(30)
            impress = Impress.Impress(self.linux)
            impress.start()
            time.sleep(15)
            impress.open(self.config.sr.files.ppt)
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
