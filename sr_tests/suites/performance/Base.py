from sr_automation.utils.TimeIt import TimeIt
from sr_automation.platform.android.Resources import Resources
from sr_automation.platform.android.applications.Mail.Mail import AndroidMail
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
from sr_automation.platform.linux.applications.Mail.Mail import LinuxMail
from sr_automation.platform.sunriver.applications.IMAPApp.IMAPApp import IMAPApp
from sr_tests.base.Base import BaseTest

from bunch import Bunch
import csv
import os
import datetime
import slash
from slash import should

from logbook import Logger
log = Logger("PerformanceBaseTest")

@slash.hooks.session_start.register
def start_performance():
    log.info("Starting performance suite")
    slash.g.resources = Resources(slash.g.sunriver.android)
    slash.g.timeit    = TimeIt()
    slash.g.collected = []

@slash.hooks.result_summary.register
def generate_csv():
    log.info("Creating CSV output")
    csv_output_path = os.path.join(slash.config.sr.paths.outputs, "measurements_{}.csv".format(slash.ctx.session.id))
    csv_file = file(csv_output_path, 'w')
    headers= [ "test"
             , "date"
             , "time"
             , "cpu_max"
             , "cpu_min"
             , "cpu_avg"
             , "mem_max"
             , "mem_min"
             , "mem_avg"
             , "bat_max"
             , "bat_min"
             , "bat_avg"
             , "bat_usage"
             ]
    csv_obj = csv.DictWriter(csv_file, headers)
    csv_obj.writeheader()
    csv_obj.writerows(slash.g.collected)
    csv_file.close()

class PerformanceBaseTest(BaseTest):
    def before(self):
        super(PerformanceBaseTest, self).before()
        self.resources = slash.g.resources
        self.timeit    = slash.g.timeit
        self.collected = slash.g.collected
        self.date      = None
    
    def after(self):
        super(PerformanceBaseTest, self).after()
        measurement = self.measurement()
        self.verify(measurement)
        self.collected.append(measurement)
    
    def measure(self):
        class wrapper(object):
            def __enter__(_self):
                self.date = str(datetime.datetime.now())
                _self.timer = self.timeit.measure()
                _self.timer.__enter__()
                _self.meter = self.resources.measure()
                _self.meter.__enter__()
            
            def __exit__(_self, type, value, tb):
                _self.timer.__exit__(None, None, None)
                _self.meter.__exit__(None, None, None)
        return wrapper()


    def measurement(self):
        measured = self.resources.measured
        return Bunch( test=self.current_test()
                    , date=self.date
                    , time=self.timeit.measured
                    , cpu_max=measured.cpu.max
                    , cpu_min=measured.cpu.min
                    , cpu_avg=measured.cpu.avg
                    , mem_max=measured.mem.max
                    , mem_min=measured.mem.min
                    , mem_avg=measured.mem.avg
                    , bat_max=measured.bat.max
                    , bat_min=measured.bat.min
                    , bat_avg=measured.bat.avg
                    , bat_usage=(measured.bat.max - measured.bat.min) / self.timeit.measured * 100 # battery usage per second
                    )

    def verify(self, measurement):
        should.be( measurement.time < self.config.sr.thresholds.time_max
                 , True
                 , "Test took too much time to complete {}".format(measurement.time)
                 )
        should.be( measurement.cpu_avg < self.config.sr.thresholds.cpu_max
                 , True
                 , "Test cpu utilization passed threshold: {}".format(measurement.cpu_avg)
                 )
        should.be( measurement.mem_avg < self.config.sr.thresholds.mem_max
                 , True
                 , "Test memory usage passed threshold: {}".format(measurement.mem_avg)
                 )
        should.be( measurement.bat_usage < self.config.sr.thresholds.bat_max
                 , True
                 , "Test battery usage passed threshold: {}".format(measurement.bat_usage)
                 )
