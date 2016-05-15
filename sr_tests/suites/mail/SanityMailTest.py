from sr_tests.base.Base import BaseTest
from sr_automation.platform.android.applications.Mail.Mail import AndroidMail
from sr_automation.platform.linux.applications.Mail.Mail import LinuxMail
from sr_automation.platform.linux.applications.Mail.GUI import LinuxMailGUI
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
from sr_automation.platform.linux.applications.Libreoffice.Calc import Calc
from datetime import datetime
from bunch import Bunch
from logbook import Logger
import time
import slash

log = Logger("Sanity Mail Suite")

@slash.hooks.session_start.register
def start_mail_sync():
    slash.g.mail = Bunch( android  = AndroidMail(slash.g.sunriver.android)
                        , linux    = LinuxMail(slash.g.sunriver.linux)
                        , email    = None
                        , password = None
                        , folder   = None
                        )

class SanityMailTest(BaseTest):
    
    DIST_PATH = "/home/BigScreen/Android/Desktop/"#config.automation_files_dir
    
    def start_android_gui(self):
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def start_linux_gui(self):
        slash.g.mail.linuxGUI = LinuxMailGUI(slash.g.sunriver.linux)
    
    def prepare_calc_file(self):
        rawInput = slash.g.sunriver.linux.ui.dogtail.rawinput
        Os = slash.g.sunriver.linux.ui.dogtail.procedural.os
        slash.g.calc = Calc(slash.g.sunriver.linux)
        slash.g.calc.start()
        full_time = str(datetime.now()).split(' ')
        date = full_time[0]
        only_time = full_time[1]
        for ch in [':','.']:
            only_time = only_time.replace(ch,'-')
        calc_file = self.DIST_PATH + date + '-' + only_time
        rawInput.typeText(date)
        time.sleep(1)
        rawInput.keyCombo('<Tab>')
        time.sleep(1)
        rawInput.typeText('Automation Text')
        time.sleep(1)
        rawInput.keyCombo('<Ctrl>s')
        time.sleep(1)
        if not Os.path.isdir(self.DIST_PATH):
            Os.mkdir(self.DIST_PATH)
        rawInput.typeText(calc_file)
        rawInput.keyCombo('<Enter>')
        calc_file += '.ods'
        return calc_file
    
    def before(self):
        super(SanityMailTest, self).before()

    def test_contacts_sync(self):
        log.info("Opening mail for sync purpose")
        slash.g.mail.linuxGUI.stop_icedove()
        self.start_android_gui()
        self.sunriver.vnc.OpenVnc()
        slash.g.mail.androidGUI.open_email_app()
        log.info("Creating contact in SIM")
        self.sunriver.desktop.openSpecificApp('Contacts')
        self.sunriver.android.ui(resourceId="com.android.contacts:id/floating_action_button").click()
        self.sunriver.android.ui(text="Create contact to SIM 1").click()
        self.sunriver.android.ui(resourceId="com.android.contacts:id/name").click()
        self.sunriver.android.ui(resourceId="com.android.contacts:id/name").set_text('automation')
        self.sunriver.android.ui(resourceId="com.android.contacts:id/number").click()
        self.sunriver.android.ui(resourceId="com.android.contacts:id/number").set_text('0547884440')
        self.sunriver.android.ui(resourceId="com.android.contacts:id/save_menu_item").click()
        log.info("Opening Icedove client")
        self.start_linux_gui()
        slash.g.mail.linuxGUI.start_icedove()
        time.sleep(7)
        ContactSynced = slash.g.mail.linuxGUI.check_contact_exists()
        time.sleep(10)
        self.sunriver.android.ui(text="automation").click()
        self.sunriver.android.ui(resourceId ="com.android.contacts:id/menu_edit").click()
        self.sunriver.android.ui(resourceId ="com.android.contacts:id/menu_delete").click()
        self.sunriver.android.ui(text="OK").click()
        slash.g.mail.linuxGUI.stop_icedove()
        self.sunriver.vnc.CloseVnc()
        assert ContactSynced == True , "Contact not found in Icedove"

    def test_mail_sync(self):
        log.info("Opening mail for sync purpose")
        slash.g.mail.linuxGUI.stop_icedove()
        self.start_android_gui()
        self.sunriver.vnc.OpenVnc()
        slash.g.mail.androidGUI.open_email_app()
        log.info("Preparing attachment file for test")
        file_to_send = self.prepare_calc_file()
        time.sleep(4)
        file_created = self.sunriver.linux.ui.dogtail.procedural.os.path.exists(file_to_send)
        log.info("Verifying file created successfully")
        assert file_created == True , "Error in creating file"
        log.info("Opening icedove")
        self.start_linux_gui()
        slash.g.mail.linuxGUI.start_icedove()
        time.sleep(15)
        log.info("Attaching file to draft")
        subject = 'Automated ' + file_to_send
        slash.g.mail.linuxGUI.send('sunriver1993@gmail.com',subject,'Mail send automatically',file_to_send)
        time.sleep(12)
        self.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>s')
        time.sleep(5)
        self.sunriver.linux.ui.dogtail.rawinput.keyCombo('<Ctrl>w')
        time.sleep(10)
        slash.g.mail.androidGUI.choose_folder('Drafts')
        time.sleep(1)
        automatedMessage = slash.g.mail.androidGUI.find_message(subject)
        log.info("Verifying mail in phone mail app")
        assert automatedMessage != False , "Cannot see draft in android"
        log.info("Sending mail")
        slash.g.mail.androidGUI.send_from_current_folder(subject)
        self.sunriver.vnc.CloseVnc()
        log.info("Verifying message arrived at Icedove")
        time.sleep(10)
        mailSent = slash.g.mail.linuxGUI.check_sent_message(subject)
        time.sleep(15)
        mailRecieved = slash.g.mail.linuxGUI.check_received_message(subject)
        slash.g.calc.stop()
        slash.g.mail.linuxGUI.stop_icedove()
        assert mailSent == True , "Mail not in sent folder"
        assert mailRecieved == True , "Mail not received"
