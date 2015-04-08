import baker
import re
import time
import os
from bunch import Bunch
import helpers as H
from subprocess import Popen, PIPE

@baker.command
def devices():
    """Show connected devices"""
    from sr_automation.platform.android.Android import Android
    print Android.devices()

def _project_root():
    return os.path.split(os.path.abspath(os.path.join(__file__, "..")))[0]

@baker.command
def project_root():
    """Show project root path"""
    print _project_root()

@baker.command
def mount_resources():
    """Mount externals directory"""
    pass

@baker.command(params={"device_id": "Device id"})
def mode_wifi(device_id = None):
    """Connect DUT over WIFI, disconnect USB"""
    devices = H.adb_devices()
    if len(devices.usb) == 0:
        return
    if device_id is not None:
        assert device_id in devices.usb
    else:
        device_id = devices.usb[0]
    
    ip = H.device_ip(device_id)
    port = 5555
    Popen(["adb", "tcpip",   "%d" % (port,)]).wait()
    time.sleep(4)
    Popen(["adb", "connect", "%s" % (ip,)]).wait()
    print "Disconnect USB cable..."
    H.wait_usb_disconnection()
    print H.adb_devices()

@baker.command(params={"device_id": "Device id"})
def mode_usb(device_id = None):
    """Connect DUT over USB, disconnect WIFI"""
    devices = H.adb_devices()
    if len(devices.ip) == 0:
        return
    if device_id is not None:
        assert device_id in devices.ip
    else:
        device_id = devices.ip[0]
    
    Popen(["adb", "disconnect"]).wait()
    print "Connect USB cable now..."
    H.wait_usb_connection()
    print H.adb_devices()

@baker.command
def screenshot():
    from sr_automation.platform.android.Android import Android
    from sr_automation.platform.sunriver.Chroot import Chroot
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    device_id = Android.devices().keys()[0]
    android = Android(device_id)
    chroot  = Chroot(android)
    chroot.run("DISPLAY=:0 gnome-screenshot -f /tmp/screenshot.png").wait()
    android.cmd("pull /data/debian/tmp/screenshot.png /tmp/screenshot.png").wait()
    import os
    os.system("feh /tmp/screenshot.png; rm -f /tmp/screenshot.png")

@baker.command
def install_dut():
    """Prepare DUT for use by automation framework"""
    from sr_automation.platform.android.Android import Android
    from sr_automation.platform.sunriver.Chroot import Chroot
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    device_id = Android.devices().keys()[0]
    android = Android(device_id)
    chroot  = Chroot(android)
    Sunriver.install(chroot)

@baker.command
def run(config, *args, **kw):
    """Run Sunriver tests with specific configuration"""
    command="SLASH_SETTINGS={} slash run {} {}".format( config
                                                      , " ".join(args)
                                                      , " ".join(["{}={}".format(k,v) for (k,v) in kw.iteritems()])
                                                      )
    os.system(command)

@baker.command
def run_suite(suite, config=None, *args, **kw):
    """
    Run Sunriver suite
    sr_tool run_suite mail Base.py  
    """
    path = os.path.join(_project_root(), "sr_tests", "suites", suite)
    if config is None:
        config = os.path.join(path, "config.py")
    command="SLASH_SETTINGS={} slash run -vvv {} {}".format( config
                                                           , " ".join(args)
                                                           , " ".join(["{}={}".format(k,v) for (k,v) in kw.iteritems()])
                                                           )
    with H.chdir(path):
        os.system(command)

def main():
    baker.run()

if __name__ == "__main__":
    main()

