from DBUSWaiter import DBUSWaiter
from DBUSWaiter import DBUSHandler
import re

class NotificationHandler(DBUSHandler):
    def __init__(self, notification_callback):
        super(NotificationHandler, self).__init__(interface = "org.freedesktop.Notifications", member = "Notify")
        self._callback = notification_callback

    def check(self, input):
        if not super(NotificationHandler, self).check(input):
            return False
        self._cached_extracted = self._callback(icon = input["args"][1], title = input["args"][2], text = input["args"][3])
        if self._cached_extracted:
            return True
        return False

    def handle(self, input):
        self._result = self._cached_extracted

class NotificationWaiter(DBUSWaiter):
    def add(self, notification_callback):
        return super(NotificationWaiter, self).add(NotificationHandler(notification_callback))

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    import sys
    address = sys.argv[1]
    port    = int(sys.argv[2])
    waiter = NotificationWaiter((address, port))
    handler = waiter.add(lambda icon, title, text: re.compile("(.*)berko", re.DOTALL).findall(text))
    waiter.start()
    with Timeout(15, False) as timeout:
        handler.wait()
        print 'result = %r' % handler.result
    waiter.stop()


