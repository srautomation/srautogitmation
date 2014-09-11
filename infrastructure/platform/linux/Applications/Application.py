import time

class _Application(object):
    def __init__(self, cmd, ui, app_cmd, app_title):
        self._cmd = cmd
        self._ldtp = ui.ldtp
        self._dogtail = ui.dogtail
        self._app_cmd = app_cmd
        self._app_title = app_title
        self._process = None

    def start(self):
        self._process = self._cmd(self._app_cmd)

    def stop(self):
        if self._process:
            self._process.terminate()
            time.sleep(2)
            if (0 != self._cmd('ls /proc/' + str(self._process.pid)).wait()): # if not killed
                self._process.kill()

    def find_children(self, app, name = None, roleName = None):
        children = app.findChildren(self._dogtail.predicate.GenericPredicate(name, roleName))
        return [(i.name, i.roleName) for i in children]

class _Editor(_Application):
    def start(self, doc = ''):
        self._app_cmd = self._app_cmd + ' ' + doc
        super(_Editor, self).start(self)
