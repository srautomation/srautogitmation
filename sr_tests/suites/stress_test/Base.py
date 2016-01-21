from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver

from bunch import Bunch
import slash

from logbook import Logger
log = Logger("StressBaseTest")

class StressBaseTest(BaseTest):

    def before(self):
        super(StressBaseTest, self).before()
    
    def open_app(self, app_name):
        log.info('Opening %s'%app_name)
        self.dogtail.procedural.run(app_name)

    def compare_cycle(self,cycle_number, cycle):
        slash.should.be(cycle_number, cycle+1)
 
#    @property
 #   def dogtial(self):
  #      return self._dogtail
