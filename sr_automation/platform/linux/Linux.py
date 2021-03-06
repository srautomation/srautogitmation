from Shell import Shell
from UI import UI

import rpyc
import time
from logbook import Logger
log = Logger("Linux")

class Linux(object):
    def __init__(self, modules, rpyc=None, modules_user=None, rpyc_user=None):
        self._modules = modules
        self._modules_user = modules_user
        self._rpyc = rpyc
        self._rpyc_user = rpyc_user
        self._shell = Shell(self._modules, self._rpyc, self._modules_user)
        if self._rpyc is not None:
            self._ip = self.cmd("netstat -na | grep ':18812.*ESTABLISHED' | head -1 | tr ':' ' ' | awk {'print $4'}", shell=True).stdout.read().strip()
        else:
            self._ip = "127.0.0.1"


    def __del__(self):
        if self._rpyc is not None:
            self._rpyc.close()

    def start(self):
        self._shell.wait_process_by_short_name("Xorg")
        time.sleep(10)
        self._ui = UI(self._shell)
        self._ui.start()

    def stop(self):
        self._ui.stop()
        self.cmd('pkill rpyc', infrastructure=True)

    @property
    def modules(self):
        return self._modules

    @property
    def shell(self):
        return self._shell

    @property
    def ui(self):
        return self._ui

    @property
    def ip(self):
        return self._ip

    def cmd(self, cmdline, *args, **kw):
        return self.shell.cmd(cmdline, *args, **kw)

if __name__ == "__main__":
    from bunch import Bunch
    import os
    import psutil
    modules = Bunch(os=os, psutil=psutil)
    
    linux = Linux(modules=modules)
    print linux.ip
    print linux.cmd("ls -la").stdout.read()
    import IPython
    IPython.embed()
