from sr_automation.platform.sunriver.Sunriver import Sunriver
from sr_automation.platform.sunriver.Resources import Resources

import os
import slash

@slash.hooks.session_start.register
def start_sunriver():
    slash.logger.info("Starting Sunriver ")
    slash.g.sunriver = Sunriver()
    slash.logger.info("Starting Desktop")
    sync_resources()

def sync_resources():
    if (("sr" not in slash.config.__dict__) or
        ("paths" not in slash.config.sr) or
        ("files" not in slash.config.sr)):
        return
    resources = Resources(slash.g.sunriver)
    for filename in slash.config.sr.files.values():
        if not resources.exists(filename):
            resources.push(os.path.join(slash.config.sr.paths.resources, filename))

@slash.hooks.result_summary.register
def stop_sunriver():
    slash.logger.info("Stopping Desktop")
    slash.g.sunriver.stop()

class BaseTest(slash.Test):
    
    def before(self):
        self.sunriver = slash.g.sunriver
        self.config   = slash.config
        self.dogtail = slash.g.sunriver.linux.ui.dogtail
        self.sunriver.vnc.CloseVnc()

    def current_test(self):
        return str(slash.ctx.test)
