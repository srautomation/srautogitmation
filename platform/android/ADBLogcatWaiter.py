from utils.PopenLineWaiter import PopenLineWaiter
from subprocess import Popen, PIPE

class ADBLogcatWaiter(PopenLineWaiter):
    def __init__(self):
        super(ADBLogcatWaiter, self).__init__(Popen(["adb", "logcat", "-v", "threadtime"], stdout = PIPE))

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    waiter = ADBLogcatWaiter()
    handler = waiter.add("^(.*)com.android.settings")
    waiter.start()
    with Timeout(15, False) as timeout:
        handler.wait()
        print 'result = %r' % handler.result
    waiter.stop()


