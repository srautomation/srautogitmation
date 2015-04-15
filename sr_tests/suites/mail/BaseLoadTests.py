from sr_tests.suites.mail.Base import MailBaseTest
import slash
import loremipsum

@slash.abstract_test_class
class BaseLoadTests(MailBaseTest):

    mail_conf = slash.config.sr.mail
    sending_load = 50

    def send_mail(self):
        raise NotImplemented

    def delete_from_sent(self):
        raise NotImplemented

    def after(self):
        self.choose_folder('sent').load()
        self.compare_all()
        self.choose_folder('trash').load()
        self.compare_all()

    def test_sending_load(self):
        for i in range(self.sending_load):
            self.send_mail(self.mail_conf.receivers,
                           loremipsum.get_sentence().encode('utf8'),
                           ' '.join(loremipsum.get_sentences(5)).encode('utf8'))

    def test_send_and_delete(self):
        for i in range(10):
            for j in range(4):
                self.send_mail(self.mail_conf.receivers,
                               loremipsum.get_sentence().encode('utf8'),
                               ' '.join(loremipsum.get_sentences(5)).encode('utf8'))
            for j in range(3):
                self.delete_from_sent()
