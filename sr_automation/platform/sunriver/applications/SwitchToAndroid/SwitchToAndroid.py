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
    import sys; sys.path.append("../../../android")
    import time
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    desktop   = DesktopInYourPocket(android)
    desktop.start()
    time.sleep(3)
    desktop.stop()

