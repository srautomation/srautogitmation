from logbook import Logger
from infrastructure.BaseTest import BaseTest
import slash

log = Logger("PerformanceBaseTest")

class PerformanceBaseTest(BaseTest):
    def measure(self, function_to_measure):
        '''
            Measures both execution time and resources consumption,
            and logs the results.
        '''
        class wrapper(object):
            def __enter__(_self):
                log.notice("Starting Measurement of action: %s" % function_to_measure.func_name)
                _self.timer = self.tester.timeit.measure()
                _self.timer.__enter__()
                _self.meter = self.device.resources.measure()
                _self.meter.__enter__()
            def __exit__(_self, type, value, tb):
                _self.timer.__exit__(None, None, None)
                _self.meter.__exit__(None, None, None)
                mes = self.device.resources.measured
                log.notice("Finished Measurement")
                log.notice("action took: %f seconds to complete" % self.tester.timeit.measured)
                slash.logger.notice("Resources measurements results:")
                slash.logger.notice("cpu: AVG=%f, MAX=%f, MIN=%f" % (mes.cpu.avg, mes.cpu.max, mes.cpu.min))        
                slash.logger.notice("memory: AVG=%d, MAX=%d, MIN=%d" % (mes.mem.avg, mes.mem.max, mes.mem.min))
                slash.logger.notice("battery: AVG=%d, MAX=%d, MIN=%d" % (mes.bat.avg, mes.bat.max, mes.bat.min))

        return wrapper()

    def verify_measurements(self, time_max, cpu_max, mem_max, batt_max):
        ''' 
            Verifies that no resource excedded its maximum value
        '''
        pass
