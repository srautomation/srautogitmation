from Base import MailBaseTest
import slash
import slash.log
import time
import loremipsum

@slash.abstract_test_class
class BaseSendTests(MailBaseTest):

    mail_conf = slash.config.sr.mail

    def send_mail(self):
        raise NotImplemented

    def after(self):
        self.choose_folder('sent')
        self.load()
        self.compare_all()
        super(BaseSendTests, self).after()

    def get_text_from_file(self, path):
        with open(path,'r') as txtfile:
            return txtfile.read()

    def test_send_regular_message(self):
        self.send_mail(self.mail_conf.receivers,
                       loremipsum.get_sentence(),
                       ' '.join(loremipsum.get_sentences(3)).encode('utf8'))

    # def test_send_pdf(self):
    #     self.send_mail(self.conf.to,
    #                    self.conf.subject,
    #                    self.conf.body,
    #                    [self.conf.filepaths.pdf])
    #
    # def test_send_docx(self):
    #     self.send_mail(self.conf.to,
    #                    self.conf.subject,
    #                    self.conf.body,
    #                    [self.conf.filepaths.docx])
    #
    # def test_send_large_file(self):
    #     self.send_mail(self.conf.to,
    #                    self.conf.subject,
    #                    self.conf.body,
    #                    [self.conf.filepaths.large])

    #def test_send_inline_pic(self):
    #    self.send_mail(self.conf.to,
    #                   self.conf.subject,
    #                   self.conf.inlinepic)

    #def test_send_link(self):
    #    self.send_mail(self.conf.to,
    #                   self.conf.subject,
    #                   self.conf.link)

    # def test_send_different_languages(self):
    #     self.send_mail(self.conf.to,
    #                    self.conf.subject,
    #                    self.get_text_from_file(self.conf.filepaths.diflangs))
    #
    #def test_send_to_mailing_list(self):
    #    self.send_mail(self.mail.linux.GetContacts(),
    #                   self.conf.subject,
    #                   self.conf.body)

    def test_send_to_self(self):
        self.send_mail(self.mail_conf.sender,
                       loremipsum.get_sentence(),
                       ' '.join(loremipsum.get_sentences(3)).encode('utf8'))

    def test_send_empty_mail(self):
        self.send_mail(self.mail_conf.receivers,
                       loremipsum.get_sentence(),
                       "")

    #def test_send_long_message(self):
    #    from loremipsum import get_paragraphs, get_paragraph
    #    howlong = 3
    #    self.send_mail(self.conf.to,
    #                   self.conf.subject,
    #                   get_paragraph())
