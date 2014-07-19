from utils.Waiter import Waiter, Handler

import glib
import dbus
from dbus.mainloop.glib import threads_init, DBusGMainLoop
from multiprocessing import Process, Pipe

class DBUSHandler(Handler):
    def __init__(self, interface, member):
        super(DBUSHandler, self).__init__()
        self._interface = interface
        self._member    = member

    @property
    def interface(self):
        return self._interface

    @property
    def member(self):
        return self._member

    def check(self, input):
        print input
        if (input["interface"] == self._interface) and (input["member"] == self._member):
            return True
        return False

    def handle(self, input):
        self._result = input["args"]


class DBUSWaiter(Waiter):
    TIMEOUT_INNER_QUEUE = 1
    def __init__(self, (address, port)):
        super(DBUSWaiter, self).__init__(self._dbus_input_method)
        DBusGMainLoop(set_as_default = True)
        self._address = address
        self._port = port
        self._bus = dbus.bus.BusConnection("tcp:host=%s,port=%d" % (self._address, self._port))
        self._bus.add_message_filter(self._dbus_handler)
    
    def start(self):
        self._pipe_write, self._pipe_read = Pipe()
        self._glib_process = Process(target = self._glib_mainloop, args = ())
        self._glib_process.start()
        super(DBUSWaiter, self).start()

    def stop(self):
        self._glib_process.terminate()
        self._pipe_write.close()
        self._pipe_read.close()
        super(DBUSWaiter, self).stop()

    def _glib_mainloop(self):
        mainloop = glib.MainLoop()
        threads_init()
        mainloop.run()

    def _dbus_handler(self, bus, message):
        self._pipe_write.send({
            "interface": message.get_interface(),
            "member":    message.get_member(),
            "args":      message.get_args_list(),
            })

    def _dbus_input_method(self):
        if self._pipe_read.poll(DBUSWaiter.TIMEOUT_INNER_QUEUE) is True:
            return self._pipe_read.recv()
        return None

    def add(self, handler):
        self._bus.add_match_string_non_blocking("eavesdrop=baaa, interface='%s', member='%s'" % (handler.interface, handler.member))
        return super(DBUSWaiter, self).add(handler)

    def remove(self, handler):
        self._bus.remove_match_string_non_blocking("eavesdrop=true, interface='%s', member='%s'" % (handler.interface, handler.member))
        return super(DBUSWaiter, self).remove(handler)

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    import sys
    address = sys.argv[1]
    port    = int(sys.argv[2])
    waiter = DBUSWaiter((address, port))
    handler = waiter.add(DBUSHandler(interface = "org.freedesktop.Notifications", member = "Notify"))
    waiter.start()
    with Timeout(15, False) as timeout:
        handler.wait()
        print 'result = %r' % handler.result
    waiter.stop()

