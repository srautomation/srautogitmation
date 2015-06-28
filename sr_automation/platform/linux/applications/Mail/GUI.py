class LinuxMailGUI(object):
    def __init__(self, linux):
        self._linux = linux
        self._dogtail = self._linux.ui.dogtail

    def send(self, to, subject, body, attachments=[]):
        to_list = ",".join(to)
        command = "thunderbird -compose \"to='{}',subject='{}',body='{}'\"".format( to_list
                                                                                  , subject
                                                                                  , body
                                                                                  )
        self._linux.shell.shell(command)


    def start_icedove(self):
        self._dogtail.procedural.run('icedove')
        self._icedove = self._dogtail.tree.root.application('Icedove')
        pwrd = self._icedove.child(roleName='dialog').child(roleName='password text') #delete those lines after the icedove password bug has been resolved
        pwrd.text = '111'                                                             #
        ok_button = self._icedove.child(roleName='dialog').child(name='OK')           #
        ok_button.click()                                                             #

    
if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    #sunriver.desktop.start()
    #sunriver.linux.start()
    mail_gui = LinuxMailGUI(sunriver.linux)
    mail_gui.start_icedove()
    import IPython
    IPython.embed()


        
