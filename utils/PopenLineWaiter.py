from TextLineWaiter import TextLineWaiter

class PopenLineWaiter(TextLineWaiter):
    def __init__(self, popen_object):
        self._popen_object = popen_object
        input_method = self._popen_object.stdout.readline
        super(PopenLineWaiter, self).__init__(input_method)

if __name__ == "__main__":
    from gevent import monkey; monkey.patch_all()
    from gevent import Timeout
    from subprocess import Popen, PIPE
    import rpyc
    rpc = rpyc.classic.connect("localhost")

    waiter = PopenLineWaiter(rpc.modules.subprocess.Popen(["cat", "/var/log/syslog"], stdout = rpc.modules.subprocess.PIPE))
    handler = waiter.add("(.*)(berko).*")
#    with waiter.wait(5) as timeout:
#        handler.wait()
#        print 'result = %r' % handler.result
    with waiter.wait(): 
        with Timeout(5, False) as timeout:
            handler.wait()
            print 'result = %r' % handler.result


