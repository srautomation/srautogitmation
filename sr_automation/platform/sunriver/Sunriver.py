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
        self._linux = self.connect(Chroot(self._android), NetInterfaces(self._android))
        self._switch_to_android =  SwitchToAndroid(self._linux, self._desktop)
        self.start()

    def start(self):
        self._desktop.start()
        self._linux.start()

    def stop(self):
        self._switch_to_android.switch()
        self._linux.stop()
        self._desktop.stop()
        self.android.ui.press.home()
    
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

    def connect(self, chroot, interfaces):
        try:
            iface = interfaces["rndis0"]
            log.info('rndis connected')
        except KeyError, e:
           # iface = interfaces["wlan0"]
            log.info('rndis not found, connecting...')
            self.android.cmd("shell service call connectivity 34 i32 0").wait()
            self.android.cmd("shell chmod 644 /sys/module/g_android/parameters/host_addr").wait()
            self.android.cmd("shell 'echo 00:01:02:03:04:05 > /sys/module/g_android/parameters/host_addr'").wait()
            self.android.cmd("shell chmod 644 /sys/module/g_android/parameters/dev_addr").wait()
            self.android.cmd("shell 'echo 00:01:02:03:04:06 > /sys/module/g_android/parameters/dev_addr'").wait()
            self.android.cmd("shell service call connectivity 34 i32 1").wait()
            self.android.cmd("wait-for-device").wait()
            self.android.cmd("shell ifconfig rndis0 up 10.42.0.2 netmask 255.255.255.0").wait()
            iface = interfaces["rndis0"]
        log.info("Starting RPyC")
        rpyc_process = chroot.run("rpyc_classic.py", shell=False)
        rpyc_user_process = chroot.run('su labuser -c "rpyc_classic.py -p 18813"', shell=False)
        log.info("Waiting RPyC")
        android = chroot._android
        while (0 == len(android.cmd('shell "netstat | grep :18812 | grep LISTEN"').stdout.read()) and
              0 == len(android.cmd('shell "netstat | grep :18813 | grep LISTEN"').stdout.read())) :
            time.sleep(0.5)
        log.info("Connecting RPyC: %r" % iface.ip)
        rpyc_user_connection = rpyc.classic.connect(iface.ip,'18813')
        rpyc_connection = rpyc.classic.connect(iface.ip)
        return Linux(modules=rpyc_connection.modules, rpyc=rpyc_connection, modules_user=rpyc_user_connection.modules, rpyc_user=rpyc_user_connection)

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
                       , "lsof"
                       , "libxml2-dev"
                       , "libxslt1-dev"
                       , "gcc"
                       ]
        PIP_PACKAGES = [ "rpyc"
                       , "psutil"
                       , "selenium"
                       , "chromedriver"
                       , "Skype4py"
                       , "lxml"
                       , "caldav"
                       , "pycarddav"
                       , "icalendar"
                       ]

        commands = "\n".join([ "apt-get -y install {}".format(" ".join(APT_PACKAGES))
                             , "pip install {}".format(" ".join(PIP_PACKAGES))
                             , "git config --global http.sslVerify false; git clone https://git.fedorahosted.org/git/dogtail.git; cd dogtail; python setup.py install; cd .. ;"
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
