import slash

class TakeSnapshot(object):
    
    @staticmethod   
    def take_snapshot(path,name):
        shell = slash.g.sunriver.linux.shell
        cmd = "gnome-screenshot -f \'%s%s\'" %(path,name)
        return_value = shell.runCommandWithReturnValue(cmd)
        return return_value
    