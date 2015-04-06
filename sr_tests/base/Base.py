from sr_automation.platform.sunriver.Sunriver import Sunriver
from sr_automation.platform.sunriver.Resources import Resources

import os
import slash

from logbook import Logger
log = Logger("BaseTest")


@slash.hooks.session_start.register
def start_sunriver():
    log.info("Starting Sunriver")
    slash.g.sunriver = Sunriver()
    log.info("Starting Desktop")
    slash.g.sunriver.desktop.start()
    slash.g.sunriver.linux.start()
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
    log.info("Stopping Desktop")
    if slash.g.sunriver.desktop.is_desktop_running():
        slash.g.sunriver.switch_to_android.switch()
    slash.g.sunriver.linux.stop()
    slash.g.sunriver.desktop.stop()

class BaseTest(slash.Test):
    def before(self):
        self.sunriver = slash.g.sunriver
