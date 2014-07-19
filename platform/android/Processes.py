import re
import time
from collections import namedtuple

class Processes(object):
    MIN_FETCH_DELAY = 0.1 # seconds
    Process = namedtuple("Process", ["name", "pid", "cpu", "mem"])
    def __init__(self, adb):
        self._adb = adb
        self._last_fetched = -1 * Processes.MIN_FETCH_DELAY
        self._parsed = None

    def _fetch(self):
        current_time = time.time()
        if (current_time < self._last_fetched + Processes.MIN_FETCH_DELAY): 
            return
        cpu_text = self._adb.cmd("shell", "dumpsys", "cpuinfo").stdout.read()
        mem_text = self._adb.cmd("shell", "dumpsys", "meminfo").stdout.read()
        cpu_temp = re.compile("\s+?(?P<percent>\d+?)% (?P<pid>\d+?)/(?P<name>.*?): ").findall(cpu_text)
        mem_temp = re.compile("\s+?(\d+?) kB: (.*?) \(pid (\d+?)\)").findall(mem_text)
        self._parsed = [Processes.Process(name = x[0][2], pid = int(x[0][1]), cpu = int(x[0][0]), mem = int(x[1][0])) for x in zip(cpu_temp, mem_temp)]

    def __getitem__(self, key):
        self._fetch()
        return self._parsed[key]

    def __len__(self):
        self._fetch()
        return len(self._parsed)

