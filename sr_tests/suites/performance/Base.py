from logbook import Logger
import datetime
import os

from BaseTest import BaseTest
from sr_automation.utils.Dumper import Dumper
import slash
from slash import config

log = Logger("PerformanceBaseTest")
conf = config.root

################################################################

SAMPLES_DESCRIPTION =   ("application", 
                        "action", 
                        "start_date", 
                        "elapsed_time", 
                        "cpu", 
                        "memory", 
                        "battery")

################################################################

class PerformanceBaseTest(BaseTest):
    def before(self):
        super(PerformanceBaseTest, self).before()
        results_file = os.path.join(conf.paths.results, conf.paths.results_file)
        self.dumper = Dumper(results_file, *SAMPLES_DESCRIPTION)
    
    def after(self):
        super(PerformanceBaseTest, self).after()
        self.dumper.save()
    
    def measure_and_verify(self, application, action, 
            cpu_max = conf.thresholds.cpu_max, 
            mem_max = conf.thresholds.mem_max, 
            bat_max = conf.thresholds.bat_max, 
            time_max = conf.thresholds.time_max):
        '''
            Measures both execution time and resources consumption,
            logs the results and validates them.
        '''
        if callable(action):        action = action.func_name
        if callable(application):   application = application.func_name

        class wrapper(object):
            def __enter__(_self):
                log.notice("Starting Measurement of action: %s.%s" % (application, action))
                _self.timer = self.tester.timeit.measure()
                _self.timer.__enter__()
                _self.meter = self.device.resources.measure()
                _self.meter.__enter__()
                _self.date = str(datetime.datetime.now())
            
            def __exit__(_self, type, value, tb):
                _self.timer.__exit__(None, None, None)
                _self.meter.__exit__(None, None, None)
                mes = self.device.resources.measured
                self.bat_usage = (mes.bat.max - mes.bat.min) / self.tester.timeit.measured * 100 # battery usage per second

                log.notice("Finished Measurement")
                log.notice("action took: %f seconds to complete" % self.tester.timeit.measured)
                slash.logger.notice("Resources measurements results:")
                slash.logger.notice("cpu: AVG=%f, MAX=%f, MIN=%f" % (mes.cpu.avg, mes.cpu.max, mes.cpu.min))        
                slash.logger.notice("memory: AVG=%d, MAX=%d, MIN=%d" % (mes.mem.avg, mes.mem.max, mes.mem.min))
                slash.logger.notice("battery: AVG=%f, MAX=%f, MIN=%f" % (mes.bat.avg, mes.bat.max, mes.bat.min))
                sample = { SAMPLES_DESCRIPTION[0] : application,
                        SAMPLES_DESCRIPTION[1] : action,
                        SAMPLES_DESCRIPTION[2] : _self.date,
                        SAMPLES_DESCRIPTION[3] : self.tester.timeit.measured,
                        SAMPLES_DESCRIPTION[4] : mes.cpu.avg,
                        SAMPLES_DESCRIPTION[5] : mes.mem.avg,
                        SAMPLES_DESCRIPTION[6] : self.bat_usage }

                self.dumper.append(**sample)
                self._verify_measurements(time_max, cpu_max, mem_max, bat_max)

        return wrapper()

    def _verify_measurements(self, time_max, cpu_max, mem_max, bat_max):
        ''' 
            Verifies that no resource excedded its maximum value
        '''
        mes = self.device.resources.measured
        if time_max:
            slash.should.be(self.tester.timeit.measured < time_max, True, 
                    "Test took too much time to complete: %f" % self.tester.timeit.measured)
            slash.should.be(mes.cpu.avg < cpu_max, True, 
                "Test cpu utilization passed threshold: %f" % mes.cpu.avg)
        slash.should.be(mes.mem.avg < mem_max, True, 
                "Test memory usage passed threshold: %f" % mes.mem.avg)
        slash.should.be(self.bat_usage < bat_max, True, 
                "Test battery usage passed threshold: %f" % self.bat_usage)

    @staticmethod
    def measure_entire_function(fn):
        def wrapper(self, *args, **kwargs):
            with self.measure_and_verify(fn.func_name, "Entire Scenario"):
                fn(self, *args, **kwargs)

        return wrapper
