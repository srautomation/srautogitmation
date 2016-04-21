import slash
import time

class LinuxMailGUI(object):
    def __init__(self, linux):
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail

    def send(self, i_To, i_Subject, i_Body, i_Attachments=[]):
        command = "icedove -compose \"to='{}',subject='{}',body='{}',attachment='{}'\"".format( i_To
                                                                                  , i_Subject
                                                                                  , i_Body
                                                                                  , i_Attachments
                                                                                  )
        slash.logger.info('Executing: '+command)
        self._linux.shell.shell(command)
       
    def start_icedove(self):
        self._dogtail.procedural.run('icedove')
        self._icedove = self._dogtail.tree.root.application('Icedove')
        try:                
            if self._icedove.child(name='Icedove - Choose User Profile', roleName='dialog') is not None:
                self._icedove.child(name='Android', roleName='list item').click()
                self._icedove.child(name='Use the selected profile without asking at startup', roleName='check box').click()
                self._icedove.child(name='Start Icedove', roleName='push button').click()
            if self._icedove.child(roleName='dialog').child(roleName='check box') is not None:
                slash.logger.info('first time dialog')
                self._icedove.child(roleName='dialog').child(roleName='check box').click()
                pwrd = self._icedove.child(roleName='dialog').child(roleName='password text')
                pwrd.text = '12srusertest'
                self._icedove.child(roleName='dialog').child(name='OK').click()
            if self._icedove.child(name='Skip this and use my existing email') is not None:
                self._icedove.child(name='Skip this and use my existing email').click()
        except:
            slash.logger.info('first dialog already entered')
    
    def stop_icedove(self):
        self._linux.cmd("killall icedove")
    
    def check_received_message(self, subject):
        self._icedove.child(name='Unread').click()
        return self._icedove.isChild(subject)
        
if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    mail_gui = LinuxMailGUI(sunriver.linux)
    mail_gui.start_icedove()
    icedove = mail_gui._dogtail.tree.root.application('Icedove')
    mail_gui.send(["dorx.libman@intel.com"], "test", "loremipsumtext")
    time.sleep(3)
    slash.logger.info('Sending mail')   
    icedove.child(name='Write: test').child(name='Send').click()
    time.sleep(3)
    pwrd = icedove.child(roleName='dialog').child(roleName='section').child('password text')
    pwrd.text = '12srusertest'
    icedove.child(roleName='dialog').child(name='OK').click()
