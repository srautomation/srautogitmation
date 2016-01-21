from sr_tests.base.Base import BaseTest
  
import slash
import IPython

class startInteractive(BaseTest):
    def test_start(self):
        IPython.embed()
