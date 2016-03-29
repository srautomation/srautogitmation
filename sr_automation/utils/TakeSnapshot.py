
class TakeSnapshot(object):
    
    def __init__(self,shell):
        self._shell = shell
        
    def take_snapshot(self,path,name):
        cmd = "gnome-screenshot -f \'%s%s\'" %(path,name)
        return_value = self._shell.runCommandWithReturnValue(cmd)
    
    