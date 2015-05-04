from subprocess import PIPE
import time

from logbook import Logger
log = Logger("LinuxShell")

class Shell(object):
    WAIT_DELAY = 0.001
    DEFAULT_ENVIRONMENT = {
            "PATH":            "/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin",
            "USER":            "root",
            "DISPLAY":         ":0.0",
            "GTK_MODULES":     "gail:atk-bridge",
            "XDG_RUNTIME_DIR": "/tmp/"}

    def __init__(self, modules, rpyc=None):
        self._modules = modules
        self._rpyc = rpyc
        self._os = self._modules.os
        self._psutil = self._modules.psutil
        if self._rpyc is not None:
            self._rpyc_process = self._psutil.Process()
            self._processes     = {self._rpyc_process.pid: self._rpyc_process}
            self._own_processes = {self._rpyc_process.pid: self._rpyc_process}
        else:
            self._processes     = {}
            self._own_processes = {}

    def cmd(self, cmdline, shell=False, env=None, infrastructure=False):
        _temp_env = self._os.environ.copy()
        _temp_env.update(Shell.DEFAULT_ENVIRONMENT)
        if env is not None:
            _temp_env.update(env)
        log.debug(cmdline)
        if not shell:
            cmdline = cmdline.split(' ')
        process = self._psutil.Popen(cmdline, shell=shell, stdout=PIPE, stderr=PIPE, env=_temp_env)
        self._processes[process.pid] = process
        if infrastructure is True:
            self._own_processes[process.pid] = process
        return process

    def shell(self, cmdline, env=None, infrastructure=False):
        return self.cmd(cmdline, shell=True, env=env, infrastructure=infrastructure)

    def is_running(self, name):
        process_list = [process for process in self._psutil.get_process_list() if process.is_running() == True]
        processes_names = [process.name() for process in process_list if process.is_running()]
        if name in processes_names:
            return True
        return False

    def wait_process(self, name):
        while True:
            if self.is_running(name):
                return True
            time.sleep(Shell.WAIT_DELAY)

    def is_pid_running(self, pid):
        return str(pid) in self._os.listdir("/proc")

    def is_running_by_short_name(self, short_name):
        return (0 == self.shell(cmdline = "cat /proc/*/stat | grep %s" % short_name, infrastructure=True).wait())

    def wait_process_by_short_name(self, short_name):
        while not self.is_running_by_short_name(short_name):
            time.sleep(Shell.WAIT_DELAY)
        return True
    
    @property
    def processes(self):
        self._processes = {pid:process for (pid, process) in self._processes.items() if self.is_running(pid)}
        return self._processes

    @property
    def own_processes(self):
        self._own_processes = {pid:process for (pid, process) in self._own_processes.items() if self.is_running(pid)}
        return self._own_processes

if __name__ == "__main__":
    from bunch import Bunch
    import os
    import psutil
    modules = Bunch(os=os, psutil=psutil)

    shell   = Shell(modules)
    p = shell.cmd("ls -la")
    print p.stdout.read()
    print shell.processes
    print shell.own_processes


