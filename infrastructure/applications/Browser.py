from selenium import webdriver
import time

from logbook import Logger
log = Logger("Browser")

class Browser(object):
    CHROMEDRIVER_RPC_PORT = 12356
    def __init__(self, linux):
        self._cmd  = cmd
        self._ip   = ip
        self._process = None
        self._driver  = None

    def start(self):
        self._process = self._cmd(["/usr/local/CHROMEDRIVER", "--port=%d" % Browser.CHROMEDRIVER_RPC_PORT, "--whitelisted-ips", "*"], shell = False)
        time.sleep(4) # TODO: change this hack
        self._driver = webdriver.Remote(desired_capabilities = webdriver.DesiredCapabilities.CHROME, command_executor = "http://%s:%d" % (self._ip, Browser.CHROMEDRIVER_RPC_PORT))
        log.info("RemoteDriver Connected")

    def stop(self):
        if self._driver is not None:
            try:
                self._driver.close()
            except Exception, e: # TODO: fix hack
                log.info(e)

    @property
    def chromium(self):
        return self._driver

