import time

class DialogOpen(object):
    @classmethod
    def open(cls, app, filepath):
        dialog = app.child(name='Open', roleName='dialog')
        if not dialog.child('Location:').showing:
            dialog.child('Type a file name').point()
            time.sleep(2)
            dialog.child('Type a file name').click()
            time.sleep(2)
        dialog.child(roleName='text').text = filepath # we want the first text box
        time.sleep(3)
        dialog.child(name='Open', roleName='push button').click()
    


