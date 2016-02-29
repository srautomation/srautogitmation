import IPython
import time

class LinuxMailGUI(object):
    def __init__(self, linux):
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail

    def send(self, to, subject, body, attachments=[]):
        to_list = ",".join(to)
        command = "icedove -compose \"to='{}',subject='{}',body='{}'\"".format( to_list
                                                                                  , subject
                                                                                  , body
                                                                                  )
        self._linux.shell.shell(command)


    def start_icedove(self):
        self._dogtail.procedural.run('icedove')
        self._icedove = self._dogtail.tree.root.application('Icedove')
        try:
            if self._icedove.child(roleName='dialog').child(roleName='check box') is not None:
                print 'first time dialog'
                pwrd = self._icedove.child(roleName='dialog').child(roleName='check box').click()
                pwrd = self._icedove.child(roleName='dialog').child(roleName='password text')
                pwrd.text = '12srusertest'
                ok_button = self._icedove.child(roleName='dialog').child(name='OK')
                ok_button.click()
        except:
            print 'first dialog already entered'

if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    mail_gui = LinuxMailGUI(sunriver.linux)
    mail_gui.start_icedove()
    icedove = mail_gui._dogtail.tree.root.application('Icedove')
    mail_gui.send(["dorx.libman@intel.com"], "test", "loremipsumtext")
    time.sleep(3)
    print 'sending mail'   
    icedove.child(name='Write: test').child(name='Send').click()
    time.sleep(3)
    pwrd = icedove.child(roleName='dialog').child(roleName='section').child('password text')
    pwrd.text = '12srusertest'
    icedove.child(roleName='dialog').child(name='OK').click()
