from Waiter import Waiter
from Waiter import Handler

import re
class TextLineHandler(Handler):
    def __init__(self, regex_pattern):
        super(TextLineHandler, self).__init__()
        self._pattern = re.compile(regex_pattern, re.DOTALL)
        self._cached_extracted = None

    def check(self, input):
        temp = self._pattern.findall(input)
        if temp:
            self._cached_extracted = temp[0]
            return True
        else:
            self._cached_extracted = None
            return False

    def handle(self, input):
        self._result = self._cached_extracted

class TextLineWaiter(Waiter):
    def __init__(self, input_method):
        super(TextLineWaiter, self).__init__(input_method)
        self._patterns = {}

    def add(self, pattern):
        assert pattern not in self._patterns
        self._patterns[pattern] = TextLineHandler(pattern)
        return super(TextLineWaiter, self).add(self._patterns[pattern])

    def remove(self, pattern):
        del self._patterns[pattern]
        return super(TextLineWaiter, self).remove(self._patterns[pattern])


if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    import subprocess
    lines_input_method = subprocess.Popen(["cat", "/proc/stat"], stdout = subprocess.PIPE).stdout.readline
    
    waiter = TextLineWaiter(lines_input_method)
    handler = waiter.add("ctxt\s+(\d+)")
    waiter.start()
    with Timeout(5, False) as timeout:
        handler.wait()
        print 'result = %r' % handler.result
    waiter.stop()

