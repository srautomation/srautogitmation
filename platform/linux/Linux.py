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
        self._processes = []
        self._env = {"DISPLAY": ":0", "GTK_MODULES": "gail:atk-bridge"}
        self._run_ldtpd()
        #self._ui = UI()

    def _export_dbus_session_address(self):
        self._dbus_address = self.cmd(r"cat /proc/$(pidof nautilus)/environ | tr '\0' '\n' | grep DBUS_SESSION_BUS_ADDRESS | cut -d '=' -f2-").stdout.read().strip()
        self._dbus_address = self._dbus_address.split(";")[0]
        self._env.update({"DBUS_SESSION_BUS_ADDRESS": self._dbus_address})
        print self._dbus_address

    def _enable_accessibility(self):
        self.cmd("gsettings set org.gnome.desktop.interface toolkit-accessibility")
        self.cmd("/usr/lib/at-spi2-core/at-spi-bus-launcher", env = self._env)
        time.sleep(3)
        self.cmd("/usr/lib/at-spi2-core/at-spi2-registryd", env = self._env).stdout.read()
        time.sleep(3)

    def _install_ldtp(self):
        self.cmd("apt-get install -y python-ldtp")

    def _run_ldtpd(self):
        #self._export_dbus_session_address()
        #self._enable_accessibility()
        self._server = self.cmd('python -c "import ldtpd; ldtpd.main()"')
        time.sleep(4)
        self._ldtp = xmlrpclib.ServerProxy("http://%s:4118" % self._ip)
        return self._ldtp
    
    @property
    def ui(self):
        return self._ui

    @property
    def ldtp(self):
        return self._ldtp

    def cmd(self, cmdline, env = None):
        return self._subprocess.Popen(cmdline, shell = True, stdout = PIPE, stderr = PIPE, env = None)

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



