import time

class _Application(object):
    def __init__(self, cmd, ui, start_cmd, stop_cmd = None):
        self._cmd = cmd
        self._ldtp = ui.ldtp
        self._dogtail = ui.dogtail
        self._start_cmd = start_cmd
        self._stop_cmd = stop_cmd
        self._process = None

    def start(self):
        self._process = self._cmd(self._start_cmd)

    def stop(self):
        if self._process:
            if self._stop_cmd:
                self._cmd(self._stop_cmd)
            else:
                self._process.terminate()
                time.sleep(2)
                if (0 != self._cmd('ls /proc/' + str(self._process.pid)).wait()): # if not killed
                    self._process.kill()

    def _find_children(self, app, name = None, roleName = None):
        children = app.findChildren(self._dogtail.predicate.GenericPredicate(name, roleName))
        return [(i.name, i.roleName) for i in children]

class _Editor(_Application):
    def start(self, doc = ''):
        self._start_cmd = self._start_cmd + ' ' + doc
        super(_Editor, self).start()
