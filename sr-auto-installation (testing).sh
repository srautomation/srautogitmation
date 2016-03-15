#!/bin/bash
## chromedriver, dogtail need internet connection in order to install correctly.

tar -xvf /media/srautomation-packages.tar.gz -C /media 

cd /media/apt-get-packages
sudo dpkg -i openssh-client_1%3a6.7p1-5+deb8u1_i386.deb openssh-server_1%3a6.7p1-5+deb8u1_i386.deb openssh-sftp-server_1%3a6.7p1-5+deb8u1_i386.deb ssh_1%3a6.7p1-5+deb8u1_all.deb libatk-bridge2.0-0_2.14.0-2_i386.deb at-spi2-core_2.14.0-1_i386.deb libatk-adaptor_2.14.0-2_i386.deb libasan1_4.9.2-10_i386.deb libc6_2.19-18+deb8u2_i386.deb libc6-dev_2.19-18+deb8u2_i386.deb libxml2_2.9.1+dfsg1-5+deb8u1_i386.deb libxml2-dev_2.9.1+dfsg1-5+deb8u1_i386.deb gconf2_3.2.6-3_i386.deb libxslt1-dev_1.1.28-2+b2_i386.deb libc-dev-bin_2.19-18+deb8u2_i386.deb libgail18_2.24.25-3_i386.deb libgail-common_2.24.25-3_i386.deb libexpat1-dev_2.1.0-6+deb8u1_i386.deb libitm1_4.9.2-10_i386.deb python-dev_2.7.9-1_i386.deb  python2.7-dev_2.7.9-2_i386.deb python-pip_1.5.6-5_all.deb python-pyatspi_2.14.0+dfsg-1_all.deb python-pyatspi2_2.14.0+dfsg-1_all.deb python-pil_2.6.1-2_i386.deb python-gobject-2_2.28.6-12_i386.deb python-gobject_3.14.0-1_all.deb statgrab_0.90-1.2_i386.deb wmctrl_1.07-7_i386.deb lsof_4.86+dfsg-1_i386.deb gcc_4%3a4.9.2-2_i386.deb gcc-4.9_4.9.2-10_i386.deb libgcc-4.9-dev_4.9.2-10_i386.deb libatomic1_4.9.2-10_i386.deb gir1.2-atspi-2.0_2.14.0-1_i386.deb libcilkrts5_4.9.2-10_i386.deb liberror-perl_0.17-1.1_all.deb libperl4-corelibs-perl_0.003-1_all.deb libpython2.7-dev_2.7.9-2_i386.deb libpython-dev_2.7.9-1_i386.deb libqt4-dbus_4%3a4.8.6+git64-g5dc8b2b+dfsg-3+deb8u1_i386.deb libqt4-xml_4%3a4.8.6+git64-g5dc8b2b+dfsg-3+deb8u1_i386.deb libqtdbus4_4%3a4.8.6+git64-g5dc8b2b+dfsg-3+deb8u1_i386.deb libstatgrab9_0.90-1.2_i386.deb libubsan0_4.9.2-10_i386.deb linux-libc-dev_3.16.7-ckt20-1+deb8u3_i386.deb python-colorama_0.3.2-1_all.deb python-distlib_0.1.9-1_all.deb python-html5lib_0.999-3_all.deb python-pexpect_3.2-1_all.deb python-setuptools_5.5.1-1_all.deb python-simplegeneric_0.8.1-1_all.deb qdbus_4%3a4.8.6+git64-g5dc8b2b+dfsg-3+deb8u1_i386.deb qt-at-spi_0.3.1-5_i386.deb qtchooser_47-gd2b7997-2_i386.deb python-lxml_3.4.0-1_i386.deb git_1%3a2.1.4-2.1+deb8u1_i386.deb git-man_1%3a2.1.4-2.1+deb8u1_all.deb

cd /media/python-packages
sudo pip install setuptools-19.7-py2.py3-none-any.whl
sudo pip install plumbum-1.6.1.post0.tar.gz
sudo pip install rpyc-3.3.0.tar.gz
sudo pip install psutil-3.4.2.tar.gz
sudo pip install selenium-2.51.1.tar.gz
sudo pip install chromedriver_installer-0.0.4.tar.gz
sudo pip install nose-1.3.7-py2-none-any.whl
sudo pip install six-1.10.0-py2.py3-none-any.whl
sudo pip install coverage-4.0.3.tar.gz
sudo pip install python_dateutil-2.4.0-py2.py3-none-any.whl
sudo pip install vobject-0.9.0.tar.gz
sudo pip install urwid-1.3.1.tar.gz
sudo pip install pyxdg-0.25.tar.gz
sudo pip install pyCardDAV-0.7.0.tar.gz
sudo pip install pytz-2015.7-py2.py3-none-any.whl
sudo pip install python_dateutil-2.4.2-py2.py3-none-any.whl
sudo pip install setuptools-20.0-py2.py3-none-any.whl
sudo pip install icalendar-3.9.2.tar.gz
sudo pip install Skype4Py-1.0.35.zip

sudo git config --global http.sslVerify false
sudo git clone --branch DOGTAIL_0_9_0 https://git.fedorahosted.org/git/dogtail.git
cd dogtail
sudo python setup.py install
cd .. 
sudo ln -s /usr/lib/i386-linux-gnu/gtk-2.0/ /usr/lib/gtk-2.0

sudo mv /media/sshd_config /etc/ssh/sshd_config 
/etc/init.d/ssh restart
sudo /etc/init.d/ssh restart

printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
printf '%*s\n' "${COLUMNS:-$(tput cols)}" '' | tr ' ' -
function box_out()
{
  local s="$*"
  tput setaf 3
  echo " -${s//?/-}------------------------------------------------------------------------------
| Follow exactly as commanded below **IP's of automation PC and phone might need adjustments				
| $(tput setaf 4)$s$(tput setaf 3)run command:"ssh automation@192.168.1.16"
| ${s//?/ }enter password:enter Yes
| ${s//?/ }enter password:"123qwe"
| ${s//?/ }on the tunnel that opens --> RUN:ssh-keygen -f "/home/automation/.ssh/known_hosts" -R [192.168.1.7]:2222
| ${s//?/ }ssh-copy-id -p 2222 BigScreen@192.168.1.7
| ${s//?/ }enter YES
 -${s//?/-}------------------------------------------------------------------------------
"
  tput sgr 0
}

box_out
