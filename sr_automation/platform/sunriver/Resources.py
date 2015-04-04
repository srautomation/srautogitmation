import os

class Resources(object):
    PATH="/data/debian/root/resources"
    def __init__(self, sunriver):
        self._sunriver = sunriver
        self._sunriver.android.cmd("shell mkdir -p {}".format(Resources.PATH))
    
    def path(self, filename):
        return os.path.join(Resources.PATH, filename)

    def push(self, local_path):
        filename = os.path.split(local_path)[1]
        self._sunriver.android.adb.cmd("push {} {}".format(local_path, self.path(filename)))

    def exists(self, filename):
        return "No such file or directory" not in self._sunriver.android.cmd("shell stat {}".format(self.path(filename))).stdout.read()

