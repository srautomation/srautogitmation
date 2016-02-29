from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Pcmanfm.Pcmanfm import Pcmanfm

from logbook import Logger
log = Logger("PCMANFM")

class PcManFMBaseTest(BaseTest):

    def before(self):
        super(PcManFMBaseTest, self).before()

    def start_pcmanfm(self):
        slash.g.pcmanfm = Pcmanfm(slash.g.sunriver.linux)
        slash.g.pcmanfm.start()

    def test_pcmanfm(self):
        self.start_pcmanfm()
        slash.g.pcmanfm.new_folder()
        slash.g.pcmanfm.new_file()
        slash.g.pcmanfm.goto('Documents')
        slash.g.pcmanfm.drag_folder()
        slash.g.pcmanfm.breadCrumbs()
        slash.g.pcmanfm.goto('Documents')
        slash.g.pcmanfm.delete_folder('Documents')

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle)
