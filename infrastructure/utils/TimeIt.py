import time

from logbook import Logger
log = Logger("TimeIt")

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
                current_time = time.time()
                log.info("measure started at: %s" % (time.ctime(current_time)))
                self._stack.append(current_time)
            def __exit__(_self, type, value, tb):
                current_time = time.time()
                log.info("measure stopped at: %s" % (time.ctime(current_time)))
                previous_time = self._stack.pop()
                self._measured = current_time - previous_time
                #if traceback is not None:
                #    raise traceback
                import traceback
                traceback.print_tb(tb)
        return wrapper()

