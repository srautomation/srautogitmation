import os

class Resources(object):
    PATH="/root" # DON'T CHANGE. some tests assume this path
                 # as they drive GUI menus to open files
    def __init__(self, sunriver):
        self._sunriver = sunriver
        self._sunriver.android.cmd("shell mkdir -p {}".format(Resources.PATH))
    
    def path(self, filename):
        return os.path.join(Resources.PATH, filename)

    def path_android(self, filename):
        return "/data/sunriver/fs/limited{}".format(self.path(filename))

    def push(self, local_path):
        filename = os.path.split(local_path)[1]
        self._sunriver.android.adb.cmd("push {} {}".format(local_path, self.path_android(filename)))

    def exists(self, filename):
        return "No such file or directory" not in self._sunriver.android.cmd("shell stat {}".format(self.path_android(filename))).stdout.read()

if __name__ == "__main__":
    from Sunriver import Sunriver
    sunriver  = Sunriver()
    resources = Resources(sunriver)
    print "Linux path: {}".format(resources.path("bobo"))
    print "Android path: {}".format(resources.path_android("bobo"))


