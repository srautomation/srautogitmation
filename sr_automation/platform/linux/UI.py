import xmlrpclib

from logbook import Logger
log = Logger("Linux.UI")

class UI(object):
    def __init__(self, rpyc, shell, ip, ldtp = None, dogtail = None, root = None, node = None):
        self._rpyc   = rpyc
        self._shell = shell
        self._ip     = ip

    def start(self):
        self._dogtail = self._rpyc.modules.dogtail
        self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)
        log.info("Connected to ldtp with xmlrpc")

    def stop(self):
        pass

    @property
    def ldtp(self):
        return self._ldtp

    @property
    def dogtail(self):
        return self._dogtail

    def run(self, name):
        self._dogtail.utils.run(name)
    
    def child(self, text = None, textContains = None, roleName = None):
       if text is not None:
           node = self._node.child(name = text)
           return UI(self._rpyc, self._shell, self._ip, ldtp = self._ldtp, dogtail = self._dogtail, root = self._root, node = node)
       else:
           raise NotImplemented

    def sibling(self, text = None):
        raise NotImplemented

    def click(self, x = None, y = None):
        if self._node is not None:
            self._node.click()

    def set_text(self, text):
        if self._node is not None:
            self._node.text = text

    def clear_text(self):
        if self._node is not None:
            self._node.text = ""

    def get_text(self):
        if self._node is not None:
            return self._ui_node.text
        return None

    def screenshot(self, filename):
        self._dogtail.utils.screenshot(filename)

    
