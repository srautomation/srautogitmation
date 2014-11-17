from sr_tests.base.BaseTest import BaseTest
from sr_automation.applications.Browser import Browser
import slash
import time
import code

class Example2(BaseTest):
    def test_play_funny_cats_video_on_youtube(self):
        with self.tester.timeit.measure():
            #time.sleep(10)
            browser = Browser(self.linux)
            browser.start()
            chrome = browser.chromium
        slash.logger.info("Open chromium took %f seconds" % (self.tester.timeit.measured))

        with self.tester.timeit.measure():
            chrome.get("http://www.youtube.com")
        slash.logger.info("youtube.com took: %f seconds" % (self.tester.timeit.measured))
#        chrome.save_screenshot("/root/1.png")

        with self.tester.timeit.measure():
            search_text = chrome.find_element_by_id("masthead-search-term")
            search_text.click()
            search_text.send_keys("funny cats")
            chrome.find_element_by_id("search-btn").click()
        slash.logger.info("Search took: %f seconds" % (self.tester.timeit.measured))
#        chrome.save_screenshot("/root/2.png")

        slash.logger.info("Waiting some time for search to happen")
        time.sleep(20) # hackish
        
        with self.tester.timeit.measure():
            funny_cats_video = chrome.find_element_by_partial_link_text("Epic")
            funny_cats_video.click()
        slash.logger.info("Funny cats video took: %f seconds" % (self.tester.timeit.measured))
#        chrome.save_screenshot("/root/4.png")
       
        time.sleep(10)
        last_strong_tag = chrome.find_elements_by_tag_name("strong")[-1]
        slash.should.be(last_strong_tag.text.endswith('Published on Feb 6, 2013'), True)
        code.interact(local = locals())
