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
            return True
        log.info('IMAPApp did not start!')
        return False

    def stop(self):
        self._sunriver.android.cmd("shell am force-stop com.example.imapapp")
        self._sunriver.linux.cmd("killall -9 imapsmtp")

if __name__ == "__main__":
    import sys; sys.path.append("../../")
    from Sunriver import Sunriver
    sunriver = Sunriver()
    imapapp = IMAPApp(sunriver)
    print imapapp.start()
