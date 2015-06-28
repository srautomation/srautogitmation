from logbook import Logger
from time import sleep
log = Logger("DesktopInYourPocket")

class DesktopInYourPocket(object):
    APP_PACKAGE = "com.intel.desktopinyourpocket"
    APP_TITLE = "Intel's Desktop In Your Pocket"
    BUTTON_START = "Start Desktop"
    BUTTON_STOP  = "Kill Desktop"
    BUTTON_SWITCH_TO_DESKTOP = "Switch To Desktop"
    def __init__(self, android):
        self._android = android

    def click_menu(self, pattern):
        log.info(pattern)
        self._android.ui.wakeup()
        self._android.cmd("shell am start -n com.intel.desktopinyourpocket/.MainActivity")
        self._android.ui(text=DesktopInYourPocket.APP_TITLE, packageName=DesktopInYourPocket.APP_PACKAGE).wait.exists()
        self._android.ui(description="More options").wait.exists()
        self._android.ui.press.menu()
        self._android.ui(textContains=pattern).click.wait()

    def openApp(self):
        if not self._android.ui(packageName="com.intel.desktopinyourpocket").exists:
            self._android.ui.press.home()
            self._android.ui(description='Apps').click()
            self._android.ui(text="Intel's Desktop In Your Pocket").click()
        

    def start(self):
        #self.click_menu(pattern=DesktopInYourPocket.BUTTON_START)
        #self._android.cmd('shell /data/srctl start')
        self.openApp()
        self._android.ui(text="Start Desktop").click()

    def stop(self):
        #self.click_menu(pattern=DesktopInYourPocket.BUTTON_STOP)
        #self._android.cmd('shell /data/srctl stop')
        self.openApp()
        self._android.ui(text="Shutdown Desktop").click()
       
    def switch_to_desktop(self):
        if not self.is_desktop_running():
            #self.click_menu(pattern=DesktopInYourPocket.BUTTON_SWITCH_TO_DESKTOP)
            log.info('Switching to desktop')
            #self._android.cmd('shell /data/srctl switch desktop')
            self.openApp()
            self._android.ui(text="Switch to Desktop").click()
            sleep(8)


    def is_desktop_running(self):
        output = self._android.cmd("shell getprop sunriver.active").stdout.read().strip()
        if len(output) == 0:
            return False
        return bool(int(output))

if __name__ == "__main__":
    from sr_automation.platform.android.Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    desktop   = DesktopInYourPocket(android)
    desktop.stop()
