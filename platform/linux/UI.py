#--------------------------------------------------
# Enable accessibilty in order to import dogtail

def enable_accessibility():
    import subprocess
    subprocess.check_output(["gsettings", "set", "org.gnome.desktop.interface", "toolkit-accessibility", "true"])

def fix_os_login_bug():
    import os
    import pwd
    os.getlogin = lambda: pwd.getpwuid(os.getuid())[0]

#enable_accessibility()
#fix_os_login_bug()
#import dogtail
#--------------------------------------------------

class UI(object):
    def __init__(self, root_application = None, ui_node = None):
        if (ui_node is None):
            if (root_application is None):
                self._root = dogtail.tree.root
            else:
                self._root = root_application
        self._ui_node = ui_node
        
    def child(self, text = None, textContains = None, roleName = None):
       if text is not None:
           ui_node = self._ui_node.child(name = text)
           return UI(ui_node)
       else:
           raise NotImplemented

    def sibling(self, text = None):
        raise NotImplemented

    def click(self, x = None, y = None):
        if self._ui_node is None:
            raise NotImplemented
        else:
            self._ui_node.click()

    def set_text(self, text):
        self._ui_node.text = text

    def clear_text(self):
        self._ui_node.text = ""

    def get_text(self):
        return self._ui_node.text

    def screenshot(self, filename):
        dogtail.utils.screenshot(filename)

    
           
