import time

class TimeIt(object):
    INVALID = 0x0FFFFFFF
    def __init__(self):
        self._stack = []
        self._measured = TimeIt.INVALID

    @property
    def measured(self):
        return self._measured

    def measure(self):
        class wrapper(object):
            def __enter__(_self):
                self._stack.append(time.time())
            def __exit__(_self, type, value, tb):
                previous_time = self._stack.pop()
                self._measured = time.time() - previous_time
                #if traceback is not None:
                #    raise traceback
                import traceback
                traceback.print_tb(tb)
        return wrapper()

