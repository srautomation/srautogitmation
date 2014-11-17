import os
import subprocess
import code

from sr_automation.Tester import Tester
import slash

from logbook import Logger
log = Logger("BaseTest")

class BaseTest(slash.Test):
    def before(self):
        self.tester = Tester()
        self.device = self.tester.device()
        self.device.start()
        self.linux = self.device.linux
        self.android = self.device.android

    def after(self):
        self.device.stop()

    def prep_resource(self, rsrc):
        'checks if rsrc is on device, if not - moves it and returns remote path'
        def exists_local(path):
            if os.path.exists(path):
                return True
            else:
                raise OSError(2, 'No such file or directory', path)

        def exists_remote(path):
            proc = self.android.adb.cmd('shell stat %s' % path)
            if proc.stdout.read().startswith("stat: can't stat"):
                return False
            else:
                return True
        
        def move(local, remote):
            proc = self.android.adb.cmd('push %s %s' % (local, remote))
            if proc.wait() == 0:
                return
            else:
                raise EnvironmentError("Couldn't Push %s to DUT at %s" % (local, remote))
        
        log.info("Preparing resource: %s" % rsrc)
        local_rsrc = os.path.join(slash.config.root.paths.resources, rsrc)
        remote_rsrc = os.path.join(slash.config.root.paths.resources_remote_adb, rsrc)
        if exists_local(local_rsrc) and not exists_remote(remote_rsrc):
            move(local_rsrc, remote_rsrc)
