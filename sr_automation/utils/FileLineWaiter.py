from TextLineWaiter import TextLineWaiter

class FileLineWaiter(TextLineWaiter):
    def __init__(self, filepath):
        self._filepath = filepath
        self._file = file(self._filepath, 'r')
        input_method = self._file.readline
        super(FileLineWaiter, self).__init__(input_method)

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    
    waiter = FileLineWaiter("/proc/stat")
    handler = waiter.add("xprocesses\s+(\d+)")
    with waiter.wait(10):
        handler.wait()
        print 'result = %r' % handler.result
