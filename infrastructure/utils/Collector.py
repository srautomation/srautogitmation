from Waiter import Waiter
from Waiter import Handler
import time

class CollectorHandler(Handler):
    def __init__(self, delay = None):
        self._delay = delay
        self._collected = []
        super(CollectorHandler, self).__init__()

    def check(self, input):
        if input:
            self.collect(input)
        if self._delay is not None:
            time.sleep(self._delay)
        return False

    def collect(self, input):
        self._collected.append((time.time(), input))

    @property
    def collected(self):
        return self._collected

class Collector(Waiter):
    collect = Waiter.wait

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    import subprocess
    lines_input_method = subprocess.Popen(["ps", "-fe"], stdout = subprocess.PIPE).stdout.readline

    collector = Collector(lines_input_method)
    handler = CollectorHandler()
    collector.add(handler)
    with collector.collect():
        time.sleep(5)
    print handler.collected
