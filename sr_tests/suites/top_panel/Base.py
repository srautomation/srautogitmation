from sr_tests.base.Base import BaseTest
from sr_automation.platform.sunriver.Sunriver import Sunriver
import time
from bunch import Bunch
import slash

from logbook import Logger
log = Logger("Search and App Launcher")

class PanelBaseTest(BaseTest):
   
    def before(self):
        super(PanelBaseTest, self).before()
    
    #list containing top panel indicators location in order - userm,applaun,sear,vol,lan,bat,BT,Wifi,sim1,sim2,time,notif,PA
    slash.g.top_panel_list = [(35,25),(110,25),(140,25),(840,25),(865,25),(900,25),(970,25),(1005,25),(1040,25),(1075,25),(1120,25),(1175,25),(1230,25)]
	
    def test_panel(self):
    	log.info("Opening Top Panel Indicators")
    	for i in slash.g.top_panel_list: 
    		slash.g.sunriver.linux.ui.dogtail.rawinput.click(i[0],i[1])
		time.sleep(3)
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(i[0],i[1])
		time.sleep(3)
		slash.g.sunriver.linux.ui.dogtail.rawinput.click(i[0],i[1])
