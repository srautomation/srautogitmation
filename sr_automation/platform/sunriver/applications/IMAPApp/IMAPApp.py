import time

from logbook import Logger
log = Logger("IMAPApp")

class IMAPApp(object):
    TITLE = "ImapApp"
    USED_PORTS = ['25', '85', '143']

    def __init__(self, sunriver):
        self._sunriver = sunriver

    def is_running(self):
        return len(self.USED_PORTS) == int(self._sunriver.linux.cmd('lsof -i :%s|grep LISTEN|grep messagebus|wc -l' % ','.join(self.USED_PORTS),shell=True).stdout.read())

    def start(self):
        if self.is_running():
            log.info('IMAPApp already running')
            return False

        username = "labuser"
        filesystem_fix_after_boot = " ; ".join([
            "USER={}".format(username)
            , "mkdir /tmp_imap 2>/dev/null"
            , "chmod 755 /tmp_imap"
            , "mount -t tmpfs none /tmp_imap"
            , "chmod 755 /tmp_imap"
            , "stat /bin/imapsmtp.bak 2>/dev/null || cp -n /bin/imapsmtp /bin/imapsmtp.bak"
            , "rm /tmp_imap/imapsmtp -rf"
            , "cp /bin/imapsmtp.bak /tmp_imap/imapsmtp"
            , "chown root:$USER /tmp_imap/imapsmtp"
            , "setcap CAP_NET_BIND_SERVICE+ep /tmp_imap/imapsmtp"
            , "chmod 110 /tmp_imap/imapsmtp"
            , "ln -sf /tmp_imap/imapsmtp /bin/imapsmtp"
            , "chown -h root:$USER /bin/imapsmtp"])
        self._sunriver.linux.shell.shell(filesystem_fix_after_boot).wait()
        self._sunriver.linux.shell.shell('su - {} -c "/home/labuser/scripts/imap_config.py &"'.format(username))
        while not self._sunriver.linux.shell.is_running_by_short_name("imap_config.py"): pass
        self._sunriver.android.cmd("shell am start -n com.example.imapapp/.TestActivity")
        time.sleep(2)
        self._sunriver.android.ui(text = IMAPApp.TITLE).wait.exists()
        if not self._sunriver.android.ui.press.home(): # try again
            time.sleep(0.5)
            self._sunriver.android.ui.press.home()
        while self._sunriver.linux.shell.is_running_by_short_name("imap_config.py"): time.sleep(0.5)
        while not self._sunriver.linux.shell.is_running_by_short_name("imapsmtp"): time.sleep(0.5)
        while not self.is_running(): time.sleep(0.5)
        return True

    def stop(self):
        self._sunriver.android.cmd("shell am force-stop com.example.imapapp")
        self._sunriver.linux.cmd("killall -9 imapsmtp")

if __name__ == "__main__":
    import sys; sys.path.append("../../")
    from Sunriver import Sunriver
    sunriver = Sunriver()
    imapapp = IMAPApp(sunriver)
    print imapapp.start()
