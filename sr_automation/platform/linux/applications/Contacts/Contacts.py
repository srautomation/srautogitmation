import time
from dateutil import parser
from bunch import Bunch
import vobject

# contacts._caldav.propfind("http://127.0.0.1:85/carddav/{}/1/".format(contacts._key), """<?xml version="1.0"?><D:propfind xmlns:D="DAV:">
# r.tree.xpath("//D:href/text()", namespaces=r.tree.nsmap)
# contacts._caldav.request(LinuxContacts.BASE_URL.format(contacts._key) + 'ev1')

# In [76]: r[0].contents
# Out[76]: 
# {u'adr': [<ADR{u'TYPE': [u'work']}\n,  >, <ADR{u'TYPE': [u'home']}\n,  >],
# u'bday': [<BDAY{}>],
# u'categories': [<CATEGORIES{}['']>],
# u'custom1': [<CUSTOM1{}>],
# u'custom2': [<CUSTOM2{}>],
# u'custom3': [<CUSTOM3{}>],
# u'custom4': [<CUSTOM4{}>],
# u'email': [<EMAIL{u'TYPE': [u'work']}ohad@wizery.com>],
# u'fn': [<FN{}Ohad Ben-Cohen>],
# u'n': [<N{} Ohad  Ben-Cohen >],
# u'nickname': [<NICKNAME{}>],
# u'note': [<NOTE{}>],
# u'org': [<ORG{}['']>],
# u'tel': [<TEL{u'TYPE': [u'work']}>,
# <TEL{u'TYPE': [u'home']}>,
# <TEL{u'TYPE': [u'cell']}>,
# <TEL{u'TYPE': [u'fax']}>,
# <TEL{u'TYPE': [u'pager']}>],
# u'title': [<TITLE{}>],
# u'url': [<URL{u'TYPE': [u'work']}>, <URL{u'TYPE': [u'home']}>],
# u'version': [<VERSION{}3.0>],
# u'x-aim': [<X-AIM{}>]}



class LinuxContacts(object):
    BASE_URL = "http://127.0.0.1:85/carddav/{}/1/"
    def __init__(self, linux):
        self._linux = linux
        self._caldav_module = self._linux._rpyc.modules.caldav

        while (0 == len(self._linux.cmd('netstat -na | grep ":85" | grep LISTEN').stdout.read())):
            time.sleep(0.5)
        
        self._key = self._read_key()
        self._caldav = self._caldav_module.DAVClient(LinuxContacts.BASE_URL.format(self._key))

    def _read_key(self):
        return self._linux.shell.shell("cat /run/imapsmtp/key").stdout.read().strip()

    def contacts(self):
        results = self._caldav.propfind("http://127.0.0.1:85/carddav/{}/1/".format(self._key), """<?xml version="1.0"?><D:propfind xmlns:D="DAV:"><D:prop><D:getcontenttype/><D:getetag/></D:prop></D:propfind>""", depth=1)
        evs = [e.rsplit('/', 1)[1] for e in results.tree.xpath("//D:href/text()", namespaces=results.tree.nsmap)]
        evs = [e for e in evs if len(e) > 0]
        evs = [self._caldav.request(LinuxContacts.BASE_URL.format(self._key) + ev) for ev in evs]
        evs = [vobject.readOne(ev.raw) for ev in evs]
        
        contacts = [Bunch(_id   = c._id,
                           name  = c.display_name,
                           phone = phones.get(c._id, ""),
                          )
                    for ev in evs
                    ]
        return evs

if __name__ == "__main__":
    import baker

    @baker.command
    def interactive():
        from sr_automation.utils.TimeIt import TimeIt
        from sr_automation.platform.sunriver.Sunriver import Sunriver
        from sr_automation.platform.sunriver.applications.IMAPApp.IMAPApp import IMAPApp
        sunriver = Sunriver()
        sunriver.desktop.start()
        imap = IMAPApp(sunriver)
        imap.start()


        contacts = LinuxContacts(sunriver.linux)
        import IPython
        IPython.embed()

        imap.stop()
        sunriver.desktop.stop()

    baker.run()

