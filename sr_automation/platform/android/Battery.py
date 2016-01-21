import re
import time

class Battery(object):
    MIN_FETCH_DELAY = 0.01 # seconds
    def __init__(self, android):
        self._android = android
        self._last_fetched = -1 * Battery.MIN_FETCH_DELAY

    def _fetch(self):
        current_time = time.time()
        if (current_time < self._last_fetched + Battery.MIN_FETCH_DELAY): 
            return
        text = self._android.cmd("shell dumpsys battery").stdout.read()
        self._last_fetched = current_time
        self._parsed = dict(re.compile("\s+(.*?)\s*?: ([^\s]+)").findall(text))

    @property
    def AC(self):
        self._fetch()
        return self._parsed["AC powered"] == "true"

    @property
    def USB(self):
        self._fetch()
        return self._parsed["USB powered"] == "true"

    @property
    def present(self):
        self._fetch()
        return self._parsed["present"] == "true"

    @property
    def health(self):
        self._fetch()
        return int(self._parsed["health"])

    @property
    def level(self):
        self._fetch()
        return int(self._parsed["level"])

    @property
    def scale(self):
        self._fetch()
        return int(self._parsed["scale"])

    @property
    def status(self):
        self._fetch()
        return int(self._parsed["status"])

    @property
    def temperature(self):
        self._fetch()
        return int(self._parsed["temperature"])

    @property
    def technology(self):
        self._fetch()
        return self._parsed["technology"]

if __name__ == "__main__":
    from Android import Android
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    battery   = Battery(android)
    print battery.level

