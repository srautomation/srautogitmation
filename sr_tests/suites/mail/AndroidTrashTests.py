from Base import MailBaseTest
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import slash.log
import IPython
import time

class AndroidTrashTests(MailBaseTest):


    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def after(self):
        if self.mail.folder != 'trash':
            self.choose_folder('trash')
            self.load()
            slash.should.be(len(self.messages.android), self.trash_count + self.number_to_delete)
        else:
            self.load()
            slash.should.be(len(self.messages.android), self.trash_count - self.number_to_delete)
        slash.logger.info("trash count OK")
        self.compare_all()
        super(AndroidDraftsTests, self).after()

    def before(self):
        super(AndroidDraftsTests, self).before()
        self.sunriver.switch_to_android.switch()
        self.choose_folder('trash')
        self.load()
        self.trash_count = len(self.messages.android)

    def test_1_delete_message_in_android(self):
        self.number_to_delete = 1
        self.choose_folder('inbox')
        slash.g.mail.androidGUI.choose_folder('inbox')
        slash.g.mail.androidGUI.delete_message()

    def test_2_delete_ten_messages_in_android(self):
        self.number_to_delete = 10
        slash.g.mail.androidGUI.choose_folder('inbox')
        self.choose_folder('inbox')
        self.load()
        if len(self.messages.android) < self.number_to_delete:
            self.number_to_delete = len(self.messages.android)
        for i in range(self.number_to_delete):
            slash.g.mail.androidGUI.delete_message()

    def test_3_delete_message_from_trash_in_android(self):
        self.number_to_delete = 1
        slash.g.mail.androidGUI.choose_folder('trash')
        slash.g.mail.androidGUI.delete_message()

    def test_4_delete_ten_messages_from_trash_in_android(self):
        self.number_to_delete = 10
        slash.g.mail.androidGUI.choose_folder('trash')
        self.choose_folder('trash')
        self.load()
        if len(self.messages.android) < self.number_to_delete:
            self.number_to_delete = len(self.messages.android)
        for i in range(self.number_to_delete):
            slash.g.mail.androidGUI.delete_message()

    def test_z_delete_all_messages_from_trash_in_android(self):
        slash.g.mail.androidGUI.choose_folder('trash')
        self.choose_folder('trash')
        self.load()
        self.number_to_delete = len(self.messages.android)
        for i in range(self.number_to_delete):
            slash.g.mail.androidGUI.delete_message()
