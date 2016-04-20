from sr_tests.base.Base import BaseTest
import slash
from sr_automation.platform.linux.applications.Pcmanfm.Pcmanfm import Pcmanfm

from logbook import Logger
log = Logger("File Manager")

class PcManFMBaseTest(BaseTest):

    def before(self):
        super(PcManFMBaseTest, self).before()

    def start_file_manager(self):
        slash.g.pcmanfm = Pcmanfm(slash.g.sunriver.linux)
        slash.g.pcmanfm.start_pcmanfm()
    
    def test_folders_in_file_manager(self):
        log.info("### Verify all default folders are available and accessible ###")
        folders = ['SDCard','Downloads','Music','Videos','Pictures','Recent files','Home','Documents']
        log.info("Starting File Manager")
        self.start_file_manager()
        AllFoldersAccessed = True
        for folder in folders:
            log.info("Accessing folder: "+folder)
            try:
                slash.g.pcmanfm.goto(folder)
            except:
                slash.add_error("Unable to access folder: "+folder)
                AllFoldersAccessed = False
                break
        log.info("Closing File Manager")
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Alt><F4>')
        slash.should.be_true(AllFoldersAccessed)

    def test_folder_manipulation(self):
        log.info("### Verifying folder manipulation on file manager ###")
        log.info("Starting File Manager")
        self.start_file_manager()
        log.info("Creating new folder")
        slash.g.pcmanfm.new_folder("Strawberries")
        #add the folder to bookmarks
        #open the folder from bookmarks
        #create a file in the created folder
        #delete it using del key
        #delete the folder
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Alt><F4>')

    def test_bread_crumbs_and_view_manipulation(self):
        log.info("### Verifying viewing manipulation of file manager ###")
        log.info("Starting File Manager")
        self.start_file_manager()
        slash.g.pcmanfm.goto('Home')
        log.info("Verifying bread crumbs")
        slash.g.pcmanfm.breadCrumbs()
        #switch to list view
        #switch back to icon view
        #maximize screen
        #open phone app, check window adjusts
        #check preview tab
        #check scroll bar exist when window is small
        slash.g.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Alt><F4>')
