import baker
import time
import os
import glob
import helpers as H
from subprocess import Popen
import sr_tools.config as config
from datetime import datetime

LOG_DIR = config.log_dir
SANITY_SUITES = config.sanity_suites

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
    Sunriver.install()

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

@baker.command
def run_sanity():
    """Run all sanity suites"""
    suites = SANITY_SUITES
    paths = []
    for suite in suites:
        path = os.path.join(_project_root(), "sr_tests", "suites", suite[0], suite[1])
        paths.append(path)
    command = "slash run -vvv"
    for path in paths:
        command += " " + path
    command += " -l " + LOG_DIR
    subpath = str(datetime.now()).split('.')[0].replace(':','-')
    command += ' -o log.session_subpath="' + subpath + '/session.log"'
    command += ' -o log.subpath="' + subpath + '/{context.test}.log"'
    os.system(command)
    fullpath = LOG_DIR + subpath + '/'
    for path in glob.iglob(os.path.join(fullpath, '<Runnable test*')):
        splitpath = path.split('.')
        newname = splitpath[6].split(':')[1] + '.' + splitpath[7].split('>')[0] + '.log'
        os.rename(path, os.path.join(fullpath, newname))

def main():
    baker.run()

if __name__ == "__main__":
    main()

