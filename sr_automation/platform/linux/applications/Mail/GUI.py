class LinuxMailGUI(object):
    def __init__(self, linux):
        self._linux = linux

    def send(self, to, subject, body, attachments=[]):
        to_list = ",".join(to)
        command = "thunderbird -compose \"to='{}',subject='{}',body='{}'\"".format( to_list
                                                                                  , subject
                                                                                  , body
                                                                                  )
        self._linux.shell.shell(command)

    
if __name__ == "__main__":
    from sr_automation.platform.sunriver.Sunriver import Sunriver
    sunriver = Sunriver()
    sunriver.desktop.start()
    sunriver.linux.start()
    mail_gui = LinuxMailGUI(sunriver.linux)
    import IPython
    IPython.embed()


        
