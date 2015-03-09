import uiautomator

class EmailGuiController(object):

    def __init__(self, device):
        self.d = device
        self.x_middle = self.d.info['displayWidth'] / 2
        self.y_bottom = self.d.info['displayHeight'] - 10
        self.y_top = 200

    def send(self, to, subject, body, attachments = []):
        self.write_mail(to, subject, body, attachments)
        self.d(resourceId = 'com.android.email:id/send').click()

    def write_mail(self, to, subject, body, attachments = []):
        self.main_view()
        self.d(resourceId = 'com.android.email:id/compose').click()
        self.d.wait.idle()
        if type(to) == type('s'):
            self.d(resourceId = 'com.android.email:id/to_content').set_text(to)
        else:
            self.d(resourceId = 'com.android.email:id/to_content').set_text(','.join(to))
        self.d(resourceId = 'com.android.email:id/subject').set_text(subject)
        self.d(resourceId = 'com.android.email:id/body').set_text(body)

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

    def main_view(self):
        self.open_email_app()
        if self.d(text = 'Settings', resourceId = 'android:id/title').exists:
            self.d.press.menu()
        while self.d(descriptionContains = 'up').exists:
            self.d(descriptionContains = 'up').click()
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

    def move_to_folder(self, contains, folder):
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
        self.main_view()
        if self.choose_message(contains):
            self.d(descriptionContains = 'delete').click()

    def enter_message(self, contains):
        self.find_message(contains).click()

    def choose_message(self, contains):
        self.find_message(contains).long_click()

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

    def scroll_down(self):
        self.d.swipe(self.x_middle, self.y_bottom, self.x_middle, self.y_top, steps = 30)
        self.d.wait.idle()

    def scroll_up(self):
        self.d.swipe(self.x_middle, self.y_top, self.x_middle, self.y_bottom, steps = 30)
        self.d.wait.idle()
    """
    def count_messages(self, folder = None):
        messages = []
        if not self.click_first_message(folder):
            return len(messages)
        self.d(resourceId = 'com.android.email:id/subject').wait.exists(timeout = 8000)
        current_m = self.d.dump()
        while len(messages) == 0 or current_m != messages[-1]:
            messages.append(current_m)
            self.scroll_to_next_message()
            self.d(resourceId = 'com.android.email:id/subject').wait.exists(timeout = 8000)
            current_m = self.d.dump()
        return len(messages)
    """

def main():
    import IPython
    am = EmailGuiController(uiautomator.device)
    IPython.embed()

if __name__ == '__main__':
    main()
