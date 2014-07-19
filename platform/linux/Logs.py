import threading

class Logs(object):
    def __init__(self, logfile_path = "/var/log/syslog"):
        self._logfile_path = logfile_path
        self._patterns = {}

    def start(self):
        pass

    def stop(self):
        pass

    def wait(pattern):
        self._patterns[pattern] = threading.Event()
        self._patterns


