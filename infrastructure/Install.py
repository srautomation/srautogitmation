
tester_commands = """
apt-get -y install build-essential python-dev python-pip ldtp android-tools-adb
pip install rpyc slash uiautomator gevent gevent-subprocess bunch
"""

DUT_commands = """
apt-get -y install at-spi2-core git gconftool-2 python-gtk2 qdbus python-pip python-pil statgrab libatk-bridge2 libatk-adaptor; #gir1.2-atk-1.0 gir1.2-gtk-3.0 
pip install rpyc psutil selenium
git clone https://github.com/lorquas/dogtail; cd dogtail; python setup.py install; cd .. ;
git clone https://github.com/ldtp/ldtp2;      cd ldtp2;   python setup.py install; cd .. ;
ln -s /usr/lib/i386-linux-gnu/gtk2.0/ /usr/lib/gtk-2.0;
"""


def install_dut():
    from Device import Device
    #device_serial = "MedfieldB60440E1"
    device = Device() #device_serial)
    print 'Installing device (this may take a few minutes...)'
    process = device._chroot_run(DUT_commands)
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
