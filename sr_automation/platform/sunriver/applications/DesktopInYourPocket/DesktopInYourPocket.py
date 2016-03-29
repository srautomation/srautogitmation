from logbook import Logger
from time import sleep
log = Logger("DesktopInYourPocket")
import time
import os

class DesktopInYourPocket(object):
    APP_PACKAGE = "com.intel.desktopinyourpocket"
    #APP_TITLE = "Intel's Desktop In Your Pocket"
    APP_TITLE = "Big Screen"
    #BUTTON_START = "Start Desktop"
    BUTTON_START = "Re_Launch Big Screen"
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

    def open_lockscreen(self):
	if not self._android.ui(resourceId="com.android.launcher:id/cell3").exists:
            os.system("adb shell input keyevent 82")
    	    os.system("adb shell input keyevent 82")

    def openApp(self):
        self.open_lockscreen()
	if not self._android.ui(text ="Big Screen").exists:
            self._android.ui.press.home()
            self._android.ui(description='Apps').click()
            sleep(2)
            if not self._android.ui(text="Big Screen").exists:
                self._android.ui(scrollable=True).scroll.horiz.backward(steps=100)
            self._android.ui(text="Big Screen").click()
        else:
            self._android.ui(text="Big Screen").click()

    def openSpecificApp(self, appName):
	self.open_lockscreen()
        self._android.ui.press.home()
        time.sleep(2)
        self._android.ui(description='Apps').click()
        time.sleep(2)
        if self._android.ui(text=appName).exists:
            self._android.ui(text=appName).click()
        elif self._android.ui(text="Calculator").exists:
            while not self._android.ui(text=appName).exists:
                self._android.ui(scrollable=True).scroll.horiz.forward(steps=100)
            self._android.ui(text=appName).click()
        else:
            while not self._android.ui(text="Calculator").exists:
                self._android.ui(scrollable=True).scroll.horiz.backward(steps=100)
            self.openSpecificApp(appName)


    def start(self):
        self.openApp()
	sleep(4)
        if self._android.ui(text = 'Get Started').exists: #incase of first time use
            self._android.ui(text = 'Get Started').click()
            self._android.ui(text = 'Next').wait.exists
            self._android.ui(text = 'Next').click()
            self._android.ui(text = 'Next').wait.exists
            self._android.ui(text = 'Next').click()
            self._android.ui(text = 'Next').wait.exists
            self._android.ui(text = 'Next').click()
            self._android.ui(text = 'Start Big Screen Experience').wait.exists
            self._android.ui(text = 'Start Big Screen Experience').click()
            sleep(2)
	    if self._android.ui(resourceId="com.intel.sunriver.ftt:id/show_again_checkbox").exists:
	    	self._android.ui(resourceId="com.intel.sunriver.ftt:id/show_again_checkbox").click()
            	sleep(2)
            	self._android.ui(resourceId='com.intel.sunriver.ftt:id/bt_devices_not_connected_dialog_ok').click()
    	    	sleep(2)
	    self._android.ui(text = "OK").wait.exists
	    self._android.ui(text = "OK").click()
        else:
            try:
		self._android.ui(text='Re-Launch Big Screen').wait.exists
                self._android.ui(text='Re-Launch Big Screen').click()
                if not self._android.ui(index='3').click():
                    self._android.ui(resourceId='com.intel.sunriver.ftt:id/bt_devices_not_connected_dialog_ok').click()
            except:
                print 'Could Not launch Sunriver'

    def stop(self):
        self._android.cmd('shell /system/sunriver/srctl stop')

    def switch_to_desktop(self):
        if not self.is_desktop_running():
            #self.click_menu(pattern=DesktopInYourPocket.BUTTON_SWITCH_TO_DESKTOP)
            log.info('Switching to desktop')
            #self._android.cmd('shell /data/srctl switch desktop')
            self.start()

    def is_desktop_running(self):
        output = self._android.cmd("shell getprop sunriver.active").stdout.read().strip()
        if len(output) == 0:
            return False
        return bool(int(output))

if __name__ == "__main__":
    from sr_automation.platform.android.Android import Android
    device_ip = Android.devices().keys()[0]
    print device_ip
    android   = Android(device_ip)
    desktop   = DesktopInYourPocket(android)
    desktop.start() 
