import slash
from Base import StressBaseTest
import uuid
import time

from logbook import Logger
log = Logger("StressBaseInsideTest")

class LibreTest(StressBaseTest):
    
    @slash.hooks.session_start.register
    def start_libre():
        slash.g.stress_run = 3 
        slash.g.app_name = 'soffice'
        log.info('Opening %s'%slash.g.app_name)
        slash.g.sunriver.linux.ui.dogtail.procedural.run(slash.g.app_name)
        slash.g._office = slash.g.sunriver.linux.ui.dogtail.tree.root.application(slash.g.app_name)
        slash.g.file_name= 'stress%s'%uuid.uuid4()
        slash.g._office.child(name='Writer Document').click()
        slasg.g.cycle = 0       

    def libre_inserter(self, soffice, cycle):
        time.sleep(4)
        textbuffer = soffice.child(roleName='paragraph')
        textbuffer.text = '%s'%cycle

    #def open_app(self, app_name):
     #   log.info('Opening %s'%app_name)
      #  slash.g.sunriver.linux.ui.dogtail.procedural.run(app_name)
        
    def save_file(self, soffice):
        soffice.child(name='Save').click()
        self.dialog=soffice.dialog('Save')
        self.dialog.child(roleName='text').text= slash.g.file_name
        self.dialog.button('Save').click()

    def save_file_already_open(self, soffice):
        soffice.child(name='Save').click()
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Alt>F4')
            
    def open_file_after_save(self, soffice):
        self.soffice = slash.g.sunriver.linux.ui.dogtail.tree.root.application(slash.g.app_name)
        time.sleep(2)
        try:
            self.soffice.child(name='Open').click()
        except:
            self.soffice.child(name='Open File').click()
        self.open_file = soffice.dialog('Open')
        self.open_file.child(name=slash.g.file_name+'.odt').click()
        self.open_file.button('Open').click()

                       
    def test_libre(self):
        for i in range(slash.g.stress_run):
            slash.logger.info("cycle #%s" % (i + 1))
            if i==0:
                self.libre_inserter(slash.g._office, self.cycle)
                self.save_file(slash.g._office)
            else:
                time.sleep(8)
                self.open_app(slash.g.app_name)
                time.sleep(2)
                self.soffice = slash.g.sunriver.linux.ui.dogtail.tree.root.application(slash.g.app_name)
                self.open_file_after_save(self.soffice)
                self.libre_inserter(self.soffice, self.cycle)
                time.sleep(2)
                self.save_file_already_open(self.soffice)
                slash.g.cycle = i
        
    def after(self):
        self.compare_cycle(slash.g.cycle)

   # def compare_cycle(self, cycle):
   #     slash.should.be(slash.g.stress_run, cycle+1)        
