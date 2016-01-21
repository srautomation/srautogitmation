import re
import time
from collections import namedtuple

class Activities(object):
    MIN_FETCH_DELAY = 0.01 # seconds
    Activity = namedtuple('Activity', ["task", "activity", "pid", "mResumed", "mStopped", "mFinished", "mLoaderStarted", "mChangingConfigurations", "mCurrentConfig"])
    def __init__(self, android):
        self._android = android 
        self._last_fetched = -1 * Activities.MIN_FETCH_DELAY
        self._parsed = None

    def _fetch(self):
        current_time = time.time()
        if (current_time < self._last_fetched + Activities.MIN_FETCH_DELAY): 
            return
        text = self._android.cmd("shell dumpsys activity top").stdout.read() 
        pattern = "ACTIVITY (.*?)/(.*?) \d.*?pid=([^\s]+).*?mResumed=([^\s]+) mStopped=([^\s]+) mFinished=([^\s]+).*?mLoadersStarted=([^\s]+).*?mChangingConfigurations=([^\s]+).*?mCurrentConfig={(.*?)}"
        temp = re.compile(pattern, re.DOTALL | re.MULTILINE).findall(text)
        self._parsed = [Activities.Activity(task = x1, activity = x2, pid = int(x3),
            mResumed = (x4 == "true"), mStopped = (x5 == "true"), mFinished = (x6 == "true"),
            mLoaderStarted = (x7 == "true"), mChangingConfigurations = (x8 == "true"),
            mCurrentConfig = x9.split(" "))
            for (x1,x2,x3,x4,x5,x6,x7,x8,x9) in temp] 

    def __getitem__(self, key):
        self._fetch()
        return self._parsed[key]

    def __len__(self):
        return len(self._parsed)


if __name__ == "__main__":
    from Android import Android
    device_id  = Android.devices().keys()[0]
    android    = Android(device_id)
    activities = Activities(android)
    print activities[0]
