import time

class AndroidCalendarGUI(object):
    def __init__(self, android):
        self._android = android
        self.d = self._android.ui
        self.x_middle = self.d.info['displayWidth'] / 2
        self.y_bottom = self.d.info['displayHeight'] - 10
        self.y_top = 200


###############################
#     Calendar app actions    #
###############################
    def create_event(self, name=None, location=None, allDay = None):
        self.open_settings_menu()
        self.d(text='New event').click()
        self.edit_event_screen(name, location, allDay)

    def delete_random_event(self):
        self.main_view()
        time.sleep(2)
        self.d(resourceId = "android:id/content").click()
        self.d(resourceId="com.android.calendar:id/info_action_delete").click()
        self.d(text='OK').click()
    
    def change_event(self, name=None, location=None, allDay = None):
        self.choose_event()
        self.d(resourceId="com.android.calendar:id/info_action_edit").click()
        self.edit_event_screen(name, location, allDay)

    def edit_event_screen(self, name, location, allDay):
        if name != None:
            self.d(resourceId="com.android.calendar:id/title").set_text('')
            self.d(resourceId="com.android.calendar:id/title").set_text(name)
            #self.d.press.back()
        if location != None:
            self.d(resourceId="com.android.calendar:id/location").set_text('')
            self.d(resourceId="com.android.calendar:id/location").set_text(location)
            #self.d.press.back()
        if allDay != None and self.is_all_day() != allDay:
            self.d(resourceId="com.android.calendar:id/is_all_day").click()
        self.d(resourceId="com.android.calendar:id/action_done").click()

    def choose_event(self):
        self.main_view()
        self.d(className="android.widget.GridLayout",instance=0).click()

#####################################
#    Navigating the calendar app    #
#####################################
    def main_view(self):
        self.open_calendar_app()
        if self.d(text="Cancel").exists:
            self.d(text="Cancel").click()
        while self.d(descriptionContains = 'Navigate up').exists:
            self.d(descriptionContains = 'Navigate up').click()
            self.d.wait.update()
        if not self.d(resourceId="com.android.calendar:id/agenda_events_list").exists:
            self.d(resourceId="com.android.calendar:id/top_button_date").click()
            self.d(text='Agenda').click()
            

    def open_calendar_app(self):
        if not self.d(packageName = 'com.android.calendar').exists:
            self.d.screen.on()
            self.d.press.home()
            self.d(description = 'Apps').click()
            self.d.wait.idle()
            if not self.d(text = 'Calendar').exists:
                self.d(text = 'Widgets').click()
                self.d(text = 'Apps').click()
            self.d(text = 'Calendar').click()

    def open_settings_menu(self):
        self.main_view()
        self.d(description='More options').click()

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

    def account_settings(self, email):
        self.main_view()
        self.d(descriptionContains="options").click()
        self.d(text="Settings").click()
        self.d(textContains=email).click()

    def is_all_day(self):
        all_day_line = 'content-desc="All day event" checkable="true" checked="true"'
        if all_day_line in self.d.dump():
            return True
        return False

if __name__ == "__main__":
    import sys; sys.path.append("../..")
    import loremipsum
    from Android import Android
    import IPython
    device_id = Android.devices().keys()[0]
    android   = Android(device_id)
    gui       = AndroidCalendarGUI(android)
    gui.create_event(name='new', location='there')
    gui.change_event(allDay=True, name='lorem')
    IPython.embed()
