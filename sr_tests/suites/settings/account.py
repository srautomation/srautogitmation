import time
from sr_tests.suites.settings.settings_Base import SettingsBaseTest
import slash
from sr_automation.utils.ImageTools import ImageTools
from sr_tools import config
import crypt
from logbook import Logger
log = Logger("ACCOUNT")


class AccountBaseTest(SettingsBaseTest):
    NEW_PASS = "123qwe!"
    NEW_USER = "test_user1"
    PRIVILAGE_USER="BigScreen"
    
    ACCOUNT_MENU_PICS = config.pictures_dir +"account_menu/"
    SAVE_PIC = ACCOUNT_MENU_PICS + "save.png"
    CHANGE_PASS_PIC = ACCOUNT_MENU_PICS + "change_password.png"
    USER_PIC = ACCOUNT_MENU_PICS + "pic.png"
    TEXTBOX_PIC = ACCOUNT_MENU_PICS + "text.png"
    DETAILS_PIC = ACCOUNT_MENU_PICS + "account_details.png"
    ACCOUNT_SNAPSHOT = "account_snapshot.png"
    
    CHANGE_PASS_PICS = ACCOUNT_MENU_PICS + "change_pass/"
    PASS_FIELDS_PIC = CHANGE_PASS_PICS + "4_fields.png"
    CANCEL_PIC = CHANGE_PASS_PICS + "cancel.png"
    SUBMIT_CHANGES_PIC = CHANGE_PASS_PICS + "submit_changes.png"
    CHANGE_PASS_SNAPSHOT = "change_pass_snapshot.png"

    def before(self):
        super(AccountBaseTest, self).before()
        self.settings = slash.g.sunriver.settings
        self.account = self.settings.account
        self.settings.start()
        self.account.enter()
    
    def test_account_changeUser(self):
        log.info("test changing username")
        old_name = self.account.get_username()
        self.change_username(self.NEW_USER)
        self.dogtail.utils.doDelay(1)
        self.account.enter() #cleanup
        self.change_username(old_name)
        
    def change_username(self,username):
        self.account.set_username(username)
        assert self.account.get_username() == username , "failed changing user"
        self.account.exit()
    
    def test_account_changePass(self):
        log.info("test changing password")
        OLD_PASS = slash.g.sunriver.currentPass
        VERIFY_PASS = self.NEW_PASS
        HINT = "123qwe!"
        pass_entries = [OLD_PASS,self.NEW_PASS, VERIFY_PASS, HINT]
        self.account.change_pass(pass_entries)
        self.checkPassword()
        pass_entries = [self.NEW_PASS,OLD_PASS ,OLD_PASS, OLD_PASS] #cleanup
        self.account.change_pass(pass_entries)
        
    def test_check_change_password_gui(self):
        self.account.change_password_click()
        ImageTools.snapShot_and_copy_file(self.CHANGE_PASS_SNAPSHOT)
        self.check_item_exist(self.PASS_FIELDS_PIC,self.CHANGE_PASS_SNAPSHOT)
        self.check_item_exist(self.CANCEL_PIC,self.CHANGE_PASS_SNAPSHOT)
        self.check_item_exist(self.SUBMIT_CHANGES_PIC,self.CHANGE_PASS_SNAPSHOT)
    
    def test_check_account_gui(self):
        log.info("test gui (picture,textbox,changePassword,Save,details) exist")
        self.account.write_in_textbox("pic_test")
        ImageTools.snapShot_and_copy_file(self.ACCOUNT_SNAPSHOT)
        self.check_item_exist(self.USER_PIC,self.ACCOUNT_SNAPSHOT)
        self.check_item_exist(self.CHANGE_PASS_PIC,self.ACCOUNT_SNAPSHOT)
        self.check_item_exist(self.SAVE_PIC,self.ACCOUNT_SNAPSHOT)
        self.check_item_exist(self.TEXTBOX_PIC,self.ACCOUNT_SNAPSHOT)
        self.check_item_exist(self.DETAILS_PIC,self.ACCOUNT_SNAPSHOT)
        
    def check_item_exist(self,submenu,snapshot): 
        submenu_name = str(submenu).rsplit('/',1)[1].rsplit('.',1)[0]
        log.info("check %s exists in  menu"%(submenu_name))
        stats = ImageTools.find_sub_image_in_image(snapshot,submenu,needToSnap=False)
        print stats
        assert stats.max_value > 0.8 , " %s wasn't in  menu" % (submenu_name)    
    
    def checkPassword(self):
        time.sleep(2)
        cmd = "echo %s | sudo -S python -c \"import spwd ;print spwd.getspnam(\'%s\')[1]\" " % (self.NEW_PASS,self.PRIVILAGE_USER)
        output = self.settings.linux.shell.runCommandWithReturnValue(cmd)
        print output
        assert crypt.crypt(self.NEW_PASS,output) == output ,"couldn't change password"
        slash.g.sunriver.currentPass = self.NEW_PASS
         
    def after(self):
        self.settings.stop()
