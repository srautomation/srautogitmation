from logbook import Logger
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

    def start(self):
        self.click_menu(pattern=DesktopInYourPocket.BUTTON_START)

    def stop(self):
        self.click_menu(pattern=DesktopInYourPocket.BUTTON_STOP)

    def switch_to_desktop(self):
        self.click_menu(pattern=DesktopInYourPocket.BUTTON_SWITCH_TO_DESKTOP)

    def is_desktop_running(self):
        output = self._android.cmd("shell getprop sunriver.active").stdout.read().strip()
        if len(output) == 0:
            return False
        return bool(int(output))

if __name__ == "__main__":
    import sys; sys.path.append("../../../android")
    import time
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    desktop   = DesktopInYourPocket(android)
    desktop.start()
    time.sleep(3)
    desktop.stop()

