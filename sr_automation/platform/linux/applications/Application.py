import time

class _Application(object):
    def __init__(self, linux, start_cmd, stop_cmd = None, dogtail_id = None, title = None):
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail
        self._start_cmd = start_cmd
        self._stop_cmd = stop_cmd
        self._process = None
        self._shell = False # TODO: handle cases of _shell=True with process group
        self._title = title # title of window, used for grab_focus()
        if dogtail_id:
            self._dogtail_id = dogtail_id # id used for dogtail.tree.root.application()
        else:
            self._dogtail_id = start_cmd
        self._app = None    # holds the accessibility object

    def start(self):
        cmd = self._start_cmd
        if not self._shell: # if shell = False, cmd has to be split
            cmd = cmd.split()
        self._process = self._linux.shell.cmd(cmd, shell = self._shell)
        time.sleep(9)
        self._app = self._dogtail.tree.root.application(self._dogtail_id)

    def stop(self):
        if self._process:
            if self._stop_cmd:
                self._linux.shell.cmd(self._stop_cmd, shell = True)
            else:
                self._process.terminate()
                time.sleep(2)
                if (self._linux.shell.is_pid_running(self._process.pid)):
                    self._process.kill()

    def _open(self, file):
        """ 
        Opens file when inside the windows manager's open dialog.
        File should be the absolute path. 
        """
        dialog = self._app.child(name = 'Open', roleName = 'dialog')
        if not dialog.child('Location:').showing:
            dialog.child('Type a file name').point()
            time.sleep(2)
            dialog.child('Type a file name').click()
            time.sleep(2)
        dialog.child(roleName = 'text').text = file # we want the first text box
        time.sleep(3)
        dialog.child(name = 'Open', roleName = 'push button').click()
    
    def _find_children(self, app, name = None, roleName = None):
        children = app.findChildren(self._dogtail.predicate.GenericPredicate(name, roleName))
        return [(i.name, i.roleName) for i in children]

    def grab_focus(self, title = None):
        '''
        Grabs focus of windows with title. 
        Title is a case-insensitive substring of the app window title.
        If title is provided it updates Application's self._title,
        otherwise self._title is used.
        '''
        if title:
            self._title = title
        if self._title:
            rc = self._linux.cmd('wmctrl -a %s' % self._title, shell = True).wait()
            if rc != 0:
                raise ValueError("wmctrl couldn't focus window with title: %s" % self._title)

class _Editor(_Application):
    def start(self, doc = ''):
        self._start_cmd = self._start_cmd + ' ' + doc
        super(_Editor, self).start()


