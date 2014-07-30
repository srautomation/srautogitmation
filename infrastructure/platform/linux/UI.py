class UI(object):
    def __init__(self, ldtp, dogtail, root = None, node = None):
        self._ldtp = ldtp
        self._dogtail = dogtail
        self._node = node
        self._root = root
        if self._root is None:
            self._root = dogtail.tree.root

    def run(self, name):
        self._dogtail.utils.run(name)
    
    def child(self, text = None, textContains = None, roleName = None):
       if text is not None:
           node = self._node.child(name = text)
           return UI(self._ldtp, self._dogtail, root = self._root, node = node)
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

    
