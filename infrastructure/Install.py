
tester_commands = """
apt-get -y install build-essential python-dev python-pip ldtp android-tools-adb
pip install rpyc slash uiautomator gevent gevent-subprocess bunch selenium
"""

DUT_commands = """
apt-get -y install at-spi2-core git ldtp gconf2 python-gtk2 python-gtk2-dev qdbus python-pip python-pil python-dev python-pyatspi2 python-gobject python-gobject-2 statgrab libatk-bridge2.0-0 libatk-adaptor;
pip install rpyc psutil selenium twisted chromedriver
git clone https://github.com/lorquas/dogtail; cd dogtail; python setup.py install; cd .. ;
ln -s /usr/lib/i386-linux-gnu/gtk-2.0/ /usr/lib/gtk-2.0;

"""


def install_dut():
    from Device import Device
    device = Device()
    print 'Installing device (this may take a few minutes...)'
    process = device._chroot_run(DUT_commands)
    while True:
        line = process.stdout.readline()
        if not line:
            break
        print line,
    process.wait()

def install_tester():
    from subprocess import Popen, PIPE
    print 'Installing tester (this may take a few minutes...)'
    process = Popen(tester_commands, shell = True)
    process.wait()
    print 'Done'

def main():
    import sys
    argument = sys.argv[1]
    if argument == "dut":
        install_dut()
    elif argument == "tester":
        install_tester()

if __name__ == "__main__":
    main()
