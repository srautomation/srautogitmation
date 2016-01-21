from sr_tests.suites.mail.Base import MailBaseTest

class TestAll(MailBaseTest):
    def test_1_all_folders_sync(self):
        folders = ['inbox', 'drafts', 'outbox', 'sent', 'trash']
        for folder in folders:
            self.choose_folder(folder)
            self.load()
            self.compare_all()
