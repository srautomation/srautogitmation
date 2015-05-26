import time
from dateutil import parser
from bunch import Bunch
from icalendar import Calendar, Event

class LinuxCalendar(object):
    BASE_URL = "http://127.0.0.1:85/caldav/{}/1/"
    def __init__(self, linux):
        self._linux = linux
        self._caldav_module = self._linux._rpyc.modules.caldav

        while (0 == len(self._linux.cmd('netstat -na | grep ":85" | grep LISTEN').stdout.read())):
            time.sleep(0.5)
        
        self._key = self._read_key()
        self._caldav = self._caldav_module.DAVClient(LinuxCalendar.BASE_URL.format(self._key))
        self._calendar = self._caldav_module.objects.Calendar(self._caldav, LinuxCalendar.BASE_URL.format(self._key))

    def _read_key(self):
        return self._linux.shell.shell("cat /run/imapsmtp/key").stdout.read().strip()

    def events(self):
        _events = [e for e in self._calendar.events() if e.url.url_raw.rsplit('/', 1)[1].startswith('ev')]
        _events = [Calendar.from_ical(e.data).subcomponents[0] for e in _events]
        events = []
        for event in _events:
            _id = event["UID"].encode('utf-8')
            title = event["SUMMARY"].encode('utf-8')
            description = event["DESCRIPTION"].encode('utf-8')
            dtstart = event["DTSTART"].dt

            if "ORGANIZER" in event.viewkeys():
                organizer = event["ORGANIZER"].split(':')[1]
            else:
                organizer = ""

            if "DTEND" in event.viewkeys():
                dtend = event["DTEND"].dt
            else:
                duration = event["DURATION"].dt
                dtend = (dtstart + duration)


            events.append(Bunch(_id = _id,
                                title = title,
                                description = description,
                                organizer = organizer,
                                dtstart = dtstart.utctimetuple(),
                                dtend   = dtend.utctimetuple(),
                                )
                            )
        return events


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


        calendar = LinuxCalendar(sunriver.linux)
        import IPython
        IPython.embed()

        imap.stop()
        sunriver.desktop.stop()

    baker.run()

