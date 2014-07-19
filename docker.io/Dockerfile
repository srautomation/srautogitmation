FROM phusion/baseimage:0.9.11 
ENV HOME /root

## Install an SSH of your choice.
#ADD test.pub /tmp/test.pub
#RUN cat /tmp/test.pub >> /root/.ssh/authorized_keys

# Install development tools
RUN apt-get update -y
RUN apt-get install -y git build-essential make gcc python python-pip python-dev ipython android-tools-adb

# Install python libraries
RUN apt-get install -y python-ldtp python-dbus 
RUN pip install gevent gevent_subprocess rpyc uiautomator uiautomatorplug

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

#EXPOSE 5037
#EXPOSE 4118

# Clean up APT when done.
#RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
