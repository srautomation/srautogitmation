from sr_automation.platform.android.Android import Android
from sr_automation.platform.android.NetInterfaces import NetInterfaces
from sr_automation.platform.linux.Linux import Linux
from sr_automation.platform.sunriver.applications.DesktopInYourPocket.DesktopInYourPocket import DesktopInYourPocket
from sr_automation.platform.sunriver.applications.SwitchToAndroid.SwitchToAndroid import SwitchToAndroid
from Chroot import Chroot
import rpyc
import time

from logbook import Logger
log = Logger("Sunriver")

class Sunriver(object):
    def __init__(self):
        self._device_id = Android.devices().keys()[0]
        self._android = Android(self._device_id)
        self._desktop = DesktopInYourPocket(self._android)
        self._linux = Sunriver.connect(Chroot(self._android), NetInterfaces(self._android))
        self._switch_to_android =  SwitchToAndroid(self._linux, self._desktop)
    
    @property
    def android(self):
        return self._android

    @property
    def linux(self):
        return self._linux

    @property
    def desktop(self):
        return self._desktop

    @property
    def switch_to_android(self):
        return self._switch_to_android

    @classmethod
    def connect(cls, chroot, interfaces):
        log.info("Starting RPyC")
        rpyc_process = chroot.run("rpyc_classic.py", shell=False)
        log.info("Waiting RPyC")
        android = chroot._android
        while (0 == len(android.cmd('shell "netstat | grep :18812 | grep LISTEN"').stdout.read())):
            time.sleep(0.5)
        try:
            iface = interfaces["rndis0"]
        except KeyError, e:
            iface = interfaces["wlan0"]
        log.info("Connecting RPyC: %r" % iface.ip)
        rpyc_connection = rpyc.classic.connect(iface.ip)
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection)

    @classmethod
    def install(cls, chroot):
        APT_PACKAGES = [ "git"
                       , "at-spi2-core"
                       , "libatk-bridge2.0-0"
                       , "libatk-adaptor"
                       , "gconf2"
                       , "python-dev"
                       , "python-pip"
                       , "python-pyatspi2"
                       , "python-gtk2"
                       , "python-gtk2-dev"
                       , "python-pil"
                       , "python-gobject"
                       , "python-gobject-2"
                       , "statgrab"
                       , "wmctrl"
                       , "libxml2-dev"
                       , "libxslt1-dev"
                       ]
        PIP_PACKAGES = [ "rpyc"
                       , "psutil"
                       , "selenium"
                       , "chromedriver"
                       , "Skype4py"
                       , "pyuserinput"
                       , "python-xlib"
                       , "lxml"
                       , "caldav"
                       , "pycarddav"
                       , "icalendar"
                       ]
        commands = "\n".join([ "apt-get -y install {}".format(" ".join(APT_PACKAGES))
                             , "pip install {}".format(" ".join(PIP_PACKAGES))
                             , "git clone https://github.com/lorquas/dogtail; cd dogtail; python setup.py install; cd .. ;"
                             , "ln -s /usr/lib/i386-linux-gnu/gtk-2.0/ /usr/lib/gtk-2.0;", # TODO: validate
                             ])
        process = chroot.run(commands)
        while True:
            line = process.stdout.readline()
            if not line: break
            print line,
        process.wait()

if __name__ == "__main__":
    import baker

    @baker.command
    def install():
        device_id = Android.devices().keys()[0]
        android = Android(device_id)
        chroot  = Chroot(android)
        Sunriver.install(chroot)

    @baker.command
    def test():
        sunriver = Sunriver()
        print sunriver

    baker.run()
