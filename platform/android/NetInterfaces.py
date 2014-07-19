import re
import time
from collections import namedtuple

class NetInterfaces(object):
    MIN_FETCH_DELAY = 0.01 # seconds
    Interface = namedtuple("Interface", ["name", "state", "ip", "mac"])
    def __init__(self, adb):
        self._adb = adb
        self._last_fetched = -1 * NetInterfaces.MIN_FETCH_DELAY

    def _fetch(self):
        current_time = time.time()
        if (current_time < self._last_fetched + NetInterfaces.MIN_FETCH_DELAY): 
            return
        text = self._adb.cmd("shell", "netcfg").stdout.read()
        self._last_fetched = current_time
        temp = re.compile("^(.+?)\s+(.+?)\s+(.+?)/(.+?)\s+([^\s]+?)\s+([^\s]+)", re.MULTILINE).findall(text)
        self._parsed = dict([(x[0], NetInterfaces.Interface(name = x[0], state = x[1], ip = x[2], mac = x[5])) for x in temp])

    def __getitem__(self, key):
        self._fetch()
        return self._parsed[key]

    def __len__(self):
        self._fetch()
        return len(self._parsed)
