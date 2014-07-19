from UI import UI
from subprocess import PIPE
import xmlrpclib
import time

class Linux(object):
    def __init__(self, ip, rpyc_connection):
        self._rpyc = rpyc_connection
        self._ip   = ip
        self._subprocess = self._rpyc.modules.subprocess
        self._ldtp = None
        self._enable_accessibility()
        self._run_ldtpd()
        #self._ui = UI()

    def _enable_accessibility(self):
        self.cmd("gsettings set org.gnome.desktop.interface toolkit-accessibility")

    def _install_ldtp(self):
        self.cmd("apt-get install -y python-ldtp")

    def _run_ldtpd(self):
        self._server = self.cmd('python -c "import ldtpd; ldtpd.main()"')
        print ("%s:4118" % self._ip)
        self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)
        self._ldtp.connect()
        return self._ldtp
    
    @property
    def ui(self):
        return self._ui

    @property
    def ldtp(self):
        return self._ldtp

    def cmd(self, cmdline):
        return self._subprocess.Popen(cmdline, shell = True, stdout = PIPE, stderr = PIPE)

    def enable_remote_dbus(self, port):
        subprocess = self._rpyc.modules.subprocess
        os = self._rpyc.modules.os
        try:
            subprocess.check_output("grep <listen>tcp /etc/dbus-1/session.conf".split(" "))
        except Exception, exc:
            extra_lines = "\\n".join([
                '  <!-- ===================================================================== -->',
                '  <listen>tcp:host=localhost,bind=*,port=%d,family=ipv4<\\/listen>' % (port),
                '  <apparmor mode="disabled"\\/>',
                '  <auth>ANONYMOUS<\\/auth>',
                '  <allow_anonymous\\/>',
                '  <!-- ===================================================================== -->',
                ])
            sed_command = ["sed", "-e", "s/\\(.*tmpdir=.*\\)/%s\\n\\1/" % (extra_lines), "/etc/dbus-1/session.conf"]
            new_data = subprocess.check_output(sed_command)
            print new_data
            f = self._rpyc.builtin.file("/etc/dbus-1/session", "w")
            f.write(new_data)
            f.close()



