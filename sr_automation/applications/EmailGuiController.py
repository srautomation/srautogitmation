import uiautomator
import time

class EmailGuiController(object):

    def __init__(self, device):
        self.d = device
        self.x_middle = self.d.info['displayWidth'] / 2
        self.y_bottom = self.d.info['displayHeight'] - 10
        self.y_top = 200

    def send(self, to, subject, body, attachments = []):
        self.choose_folder('outbox')
        self.write_mail(to, subject, body, attachments)
        self.d(resourceId = 'com.android.email:id/send').click()
        if not body:
            self.d(text="Send").click()
        self.wait_outbox_empty()

    def write_mail(self, to, subject, body, attachments = []):
        self.main_view()
        self.d(resourceId = 'com.android.email:id/compose').click()
        self.d.wait.idle()
        if isinstance(to, basestring):
            self.d(resourceId = 'com.android.email:id/to_content').set_text(to)
        else:
            self.d(resourceId = 'com.android.email:id/to_content').set_text(','.join(to))
        self.d(resourceId = 'com.android.email:id/subject').set_text(subject)
        body_textbox = self.d(resourceId="com.android.email:id/body")
        body_textbox.set_text(body)

    def save_draft(self, to = '', subject = '', body = '', attachments = []):
        self.write_mail(to, subject, body, attachments)
        self.d.press.menu()
        self.d(text = 'Save draft').click()
        self.main_view()

    def send_from_drafts(self, contains):
        self.choose_folder('drafts')
        self.enter_message(contains)
        self.d(descriptionContains = 'edit').click()
        self.d(resourceId = 'com.android.email:id/send').click()

    def reply(self, body):
        self.d(resourceId = "com.android.email:id/reply").click()
        self.d(text = "Compose email").set_text(body)
        self.d(resourceId = 'com.android.email:id/send').click()

    def reply_all(self, body):
        self.d(description = "More options", resourceId = "com.android.email:id/overflow").click()
        self.d(text = "Reply all").click()
        self.d(text = "Compose email").set_text(body)
        self.d(resourceId = 'com.android.email:id/send').click()

    def forward(self, to, body):
        self.d(description = "More options", resourceId = "com.android.email:id/overflow").click()
        self.d(text = "Forward").click()
        self.d(text = "To").set_text(to)
        self.d(text = "Compose email").set_text(body)
        self.d(resourceId = 'com.android.email:id/send').click()

    def main_view(self):
        self.open_email_app()
        if self.d(text = 'Settings', resourceId = 'android:id/title').exists:
            self.d.press.menu()
        while self.d(descriptionContains = 'Navigate up').exists:
            self.d(descriptionContains = 'Navigate up').click()
            self.d.wait.update()
        if self.d(resourceId = 'android:id/action_mode_close_button').exists:
            self.d(resourceId = 'android:id/action_mode_close_button').click()
        self.close_drawer()

    def open_email_app(self):
        if not self.d(packageName = 'com.android.email').exists:
            self.d.screen.on()
            self.d.press.home()
            self.d(description = 'Apps').click()
            self.d.wait.idle()
            if not self.d(text = 'Email').exists:
                self.d(text = 'Widgets').click()
                self.d(text = 'Apps').click()
            self.d(text = 'Email').click()

    def choose_folder(self, folder):
        self.main_view()
        if not self.d(textContains = folder, resourceId = 'android:id/action_bar_title'):
            self.open_drawer()
            if self.d(textContains = folder, resourceId = 'com.android.email:id/name').exists:
                self.d(textContains = folder, resourceId = 'com.android.email:id/name').click()
                return True
            self.d(resourceId = 'android:id/list', className = 'android.widget.ListView').swipe.up()
            if self.d(textContains = folder, resourceId = 'com.android.email:id/name').exists:
                self.d(textContains = folder, resourceId = 'com.android.email:id/name').click()
                return True
            return False
        return True

    def choose_account(self, account):
        self.main_view()
        if not self.d(textContains = account, resourceId = 'android:id/action_bar_subtitle'):
            self.open_drawer()
            if self.d(textContains = account, resourceId = 'com.android.email:id/name').exists:
                self.d(textContains = account, resourceId = 'com.android.email:id/name').click()
                return True
            self.d(resourceId = 'android:id/list', className = 'android.widget.ListView').swipe.down()
            if self.d(textContains = account, resourceId = 'com.android.email:id/name').exists:
                self.d(textContains = account, resourceId = 'com.android.email:id/name').click()
                return True
            return False
        return True

    def move_message_to_folder(self, contains, folder):
        self.choose_message(contains)
        self.d(description = 'Move to').click()
        self.d(resourceId = 'android:id/select_dialog_listview').swipe.down()
        if self.d(textContains = folder).exists:
            self.d(textContains = folder).click()
            return True
        self.d(resourceId = 'android:id/select_dialog_listview').swipe.up()
        if self.d(textContains = folder).exists:
            self.d(textContains = folder).click()
            return True

    def refresh_mail(self, folder = None):
        if folder != None:
            self.choose_folder(folder)
        self.d.press.menu()
        self.d(text = 'Refresh').click()
        self.d(className = 'android.widget.ProgressBar').wait.gone(timeout = 10000)

    def open_drawer(self):
        if self.d(descriptionContains = 'close nav').exists:
            self.d(descriptionContains = 'close nav').click()

    def close_drawer(self):
        if self.d(descriptionContains = 'open nav').exists:
            self.d(descriptionContains = 'open nav').click()

    def scroll_to_top(self):
        if self.d(resourceId = 'android:id/list', className = 'android.widget.ListView').exists:
            self.d(resourceId = 'android:id/list', className = 'android.widget.ListView').swipe.down()

    def scroll_to_next_message(self):
        self.d(resourceId = 'com.android.email:id/subject').swipe.left(steps = 2)

    def wait(self, cycles = 1):
        for i in range(cycles):
            self.d.wait.update()
            self.d.wait.idle()

    def click_first_message(self, folder = None):
        if folder != None:
            self.choose_folder(folder)
        self.d(descriptionContains = 'conversation').wait.exists(timeout = 10000)
        if not self.d(descriptionContains = 'conversation').exists:
            return False
        self.d(resourceId = 'android:id/list').swipe.down(steps = 2)
        self.d.wait.idle()
        self.d(descriptionContains = 'conversation', instance = 0).click()
        return True

    def search(self, term):
        self.main_view()
        self.d(descriptionContains = 'search').click()
        self.d(resourceId = 'android:id/search_src_text').set_text(term)
        self.d.press.enter()

    def delete_message(self, contains):
        if self.choose_message(contains):
            self.d(descriptionContains = 'delete').click()

    def delete_first_message(self):
        self.choose_first_message()
        self.d(descriptionContains = 'delete').click()

    def delete_from_trash(self, contains):
        self.choose_folder('trash')
        self.delete_message(contains)

    def delete_first_from_trash(self):
        self.choose_folder('trash')
        self.delete_first_message()

    def enter_message(self, contains):
        self.find_message(contains).click()

    def choose_message(self, contains):
        self.find_message(contains).long_click()

    def choose_first_message(self):
        self.d(resourceId="android:id/list").child(index="0").long_click()

    def find_message(self, contains):
        if self.d(descriptionContains = contains).exists:
            return self.d(descriptionContains = contains)
        prev = self.d.dump()
        self.scroll_down()
        new = self.d.dump()
        while new != prev:
            if self.d(descriptionContains = contains).exists:
                return self.d(descriptionContains = contains)
            prev = self.d.dump()
            self.scroll_down()
            new = self.d.dump()
        return False

    def mark_as_read(self, contains):
        self.choose_message(contains)
        if self.d(description = 'Mark read').exists:
            self.d(description = 'Mark read').click()
        self.d.press.back()

    def mark_as_unread(self, contains):
        self.choose_message(contains)
        if self.d(description = 'Mark unread').exists:
            self.d(description = 'Mark unread').click()
        self.d.press.back()

    def add_star(self):
        self.choose_first_message()
        self.d(descriptionContains="options").click()
        self.d(text="Add star").click()
        self.d.press.back()

    def remove_star(self):
        self.choose_first_message()
        self.d(descriptionContains="options").click()
        self.d(text="Remove star").click()
        self.d.press.back()

    def add_account(self, email, password):
        self.main_view()
        self.d(description = "More options", className = "android.widget.ImageButton").click()
        self.d(text="Settings").click()
        self.d(text="Add account").click()
        self.d(text="Email address").set_text(email)
        self.d(resourceId="com.android.email:id/account_password").set_text(password)
        self.d(text="Next").click()
        while self.d(textContains="Validating server settings").exists: pass
        self.d(text="Next").click()
        while self.d(textContains="creating account").exists: pass
        self.d(text="Next").click()

    def remove_account(self, email):
        self.d.press.home()
        self.d.open.quick_settings()
        self.d(textContains='settings').click()
        self.wait()
        self.scroll_down()
        self.d(text="IMAP").click()
        self.d(text=email).click()
        self.d(descriptionContains="options").click()
        self.d(text="Remove account").click()
        self.d(text="Remove account").click()

    def scroll_down(self):
        self.d.swipe(self.x_middle, self.y_bottom, self.x_middle, self.y_top, steps = 30)
        self.d.wait.idle()

    def scroll_up(self):
        self.d.swipe(self.x_middle, self.y_top, self.x_middle, self.y_bottom, steps = 30)
        self.d.wait.idle()

    def account_settings(self, email):
        self.main_view()
        self.d(descriptionContains="options").click()
        self.d(text="Settings").click()
        self.d(textContains=email).click()

    def change_name(self, email, name):
        self.account_settings(email)
        self.d(text="Your name").click()
        self.d(resourceId="android:id/edit").set_text(name)
        self.d(text="OK").click()
        self.main_view()

    def change_sig(self, email,  sig):
        self.account_settings(email)
        self.d(text="Signature").click()
        self.d(resourceId="android:id/edit").set_text(sig)
        self.d(text="OK").click()
        self.main_view()

    def wait_outbox_empty(self):
        self.choose_folder('outbox')
        #self.d(text="No messages.").wait.exists()
        while not self.d(text="No messages.").exists: pass


def main():
    import IPython, loremipsum, time
    am = EmailGuiController(uiautomator.device)
    to='srusertest@gmail.com'
    for i in range(12):
        am.send(to, loremipsum.get_sentence().encode('utf8')," ".join(loremipsum.get_sentences(4)).encode('utf8'))
    #IPython.embed()

if __name__ == '__main__':
    main()
