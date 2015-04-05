import time
from logbook import Logger
log = Logger("SwitchToAndroid")

class SwitchToAndroid(object):
    def __init__(self, linux):
        self._linux = linux

    def switch(self):
        log.info('Switching to android')
        mouse = self._linux.ui.pymouse
        scx, scy = mouse.screen_size()
        mouse.click(scx - 20, 20)
        time.sleep(1)
        mouse.click(7 * scx / 12, 7 * scy / 12)

if __name__ == "__main__":
    from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    import sys; sys.path.append("../../../android")
    from Android import Android
    sunriver = Sunriver()
    sunriver.desktop.start()
    time.sleep(3)
    sunriver.linux.start()
    switcher = SwitchToAndroid(sunriver.linux)
    switcher.switch()
    sunriver.desktop.stop()

