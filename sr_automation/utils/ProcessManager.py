import slash
from logbook import Logger
from __builtin__ import False
log = Logger("ProcessManager")

class ProcessManager(object):
    
    @staticmethod
    def convert_app_name_to_pid(i_appName):
        cmd = "ps -ef | grep -i "+i_appName+" |grep -v grep |awk '{print $2}'"
        appPid = slash.g.sunriver.linux.shell.runCommandWithReturnValue(cmd)
        log.info(i_appName+"'s PID is "+appPid)
        try:
            returnValue = int(appPid)
        except ValueError:
            returnValue = None
        return returnValue
    
    @staticmethod
    def check_app_by_pid(i_appPid):
        try:
            slash.g.sunriver.linux.ui.dogtail.procedural.os.kill(i_appPid, 0)
        except OSError:
            return False
        else:
            return True
        
    @staticmethod
    def verify_app_runnning(i_appName):
        running = True
        if int(slash.g.sunriver.linux.shell.runCommandWithReturnValue("ps -ef |grep '"+i_appName+"' |grep -v grep |wc -l")) == 0:
            running = False
        return running

