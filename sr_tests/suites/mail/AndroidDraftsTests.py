from sr_tests.suites.mail.Base import MailBaseTest
from sr_automation.platform.android.applications.Mail.GUI import AndroidMailGUI
import slash
import slash.log
import IPython
import time
import loremipsum

class AndroidDraftsTests(MailBaseTest):

    mail_conf = slash.config.sr.mail

    @slash.hooks.session_start.register
    def start_android_gui():
        slash.g.mail.androidGUI = AndroidMailGUI(slash.g.sunriver.android)

    def after(self):
        self.choose_folder('drafts')
        self.load()
        slash.should.be(len(self.messages.android), self.drafts_counts + 1)
        slash.logger.info("Drafts count OK")
        self.compare_all()
        super(AndroidDraftsTests, self).after()

    def before(self):
        super(AndroidDraftsTests, self).before()
        if slash.g.sunriver.desktop.is_desktop_running():
            slash.g.sunriver.switch_to_android.switch()
        self.choose_folder('drafts')
        self.load()
        self.drafts_counts = len(self.messages.android)

    def test_save_regular_draft(self):
        slash.g.mail.androidGUI.send(self.mail_conf.receivers,
                                     loremipsum.get_sentence().encode('utf8'),
                                     ' '.join(loremipsum.get_sentences(3)).encode('utf8'),
                                     to_drafts=True)

    def test_save_reply_draft(self):
        self.click_first_in_inbox()
        slash.g.mail.androidGUI.reply(' '.join(loremipsum.get_sentences(3)).encode('utf8'),
                                      to_drafts=True)

    def test_save_forward_draft(self):
        self.click_first_in_inbox()
        slash.g.mail.androidGUI.forward(self.mail_conf.receivers,
                                        ' '.join(loremipsum.get_sentences(3)).encode('utf8'),
                                        to_drafts=True)

    def click_first_in_inbox(self):
        slash.g.mail.androidGUI.choose_folder('inbox')
        slash.g.mail.androidGUI.choose_message()

    # def test_save_hebrew_draft(self)
    # def test_save_hindi_draft(self)
