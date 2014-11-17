import threading

class Handler(object):
    def __init__(self):
        self._done = threading.Event()
        self._result = None

    @property
    def active(self):
        return not self._done.is_set()

    @property
    def result(self):
        return self._result

    def deactivate(self):
        self._done.set()

    def wait(self, timeout = None):
        self._done.wait(timeout)

    def check(self, input):
        return False

    def handle(self, input):
        pass

class Waiter(object):
    TIMEOUT_JOIN = 5.0 # seconds
    DELAY_WAIT   = 0.01 # seconds

    def __init__(self, input_method):
        self._input_method = input_method
        self._handlers = []
        self._stopped = threading.Event()
        self._last_input = None

    def start(self):
        self._thread = threading.Thread(target = self._mainloop)
        self._stopped.clear()
        self._thread.start()
        return self

    def stop(self):
        self._stopped.set()
        self._thread.join(Waiter.TIMEOUT_JOIN)
        return self

    def wait(self, timeout = 0):
        class WaiterTimeout(object):
            def __init__(_self, timeout):
                pass 
            def __enter__(_self):
                self.start()
            def __exit__(_self, type, value, traceback):
                self.stop()
        return WaiterTimeout(timeout)

    def add(self, handler):
        self._handlers.append(handler)
        return handler

    def remove(self, handler):
        self._handlers.remove(handler)
        return handler

    def _mainloop(self):
        while not self._stopped.wait(Waiter.DELAY_WAIT):
            self._last_input = self._input_method()
            if self._last_input is None:
                continue
            for handler in self._handlers:
                if handler.active is False:
                    continue
                if handler.check(self._last_input):
                    handler.handle(self._last_input)
                    handler.deactivate()
