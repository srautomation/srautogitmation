from utils import FileLineWaiter

class Syslog(object):
    SYSLOG_PATH = "/var/log/syslog"


    def __init__(self, patterns):
        self._patterns = patterns

    def __enter__(self):
        self._syslog_waiter = FileLineWaiter("/v
