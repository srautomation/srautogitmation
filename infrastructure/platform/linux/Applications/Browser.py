class Browser(object):
    def __init__(self, rpyc_connection):
        self._rpyc = rpyc_connection
        self._webdriver = self._rpyc.modules["selenium", "webdriver"]
        self._driver = None
        self._current_page = None

    def start(self):
        self._driver = self._webdriver.Firefox()

    def go(self, uri):
        self._driver.get(uri)

    def link(self, text):
        return self._driver.find_elements_by_partial_link_text(text)[0]

    def text(self, initial_value = None, near_position = None):
        if initial_value is not None:
            results = [x for x in self._driver.find_elements_by_css_selector("input") if x.get_attribute("value") == initial_value]
            if len(results) == 0:
                return None
            return results[0]

        elif near_position is not None:
            pass

        return None


