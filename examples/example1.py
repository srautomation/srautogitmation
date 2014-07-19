from Tester import Tester
tester = Tester()

#------------------------------------------------------
# This test prints device battery percentage,
# then runs libreoffice and waits for the gui to be 
# visible. It measures how long it took libreoffice
# to appear.
# The test passes successfully if it takes less than
# 5 seconds for libreoffice to appear
#
# example output:
# 09:02 barak@berkos:/media/x/home/barak/Development/wizery/Intel/SunRiver/automation (master) $ python examples/example1.py  
# 99
# 0.0705978870392

def test1(tester):
    with tester.device("MedfieldB60440E1") as device:
        print device.android.battery.level
        with tester.timeit.measure():
            device.linux.ldtp.launchapp("libreoffice")
            device.linux.ldtp.waittillguiexist("*LibreOffice*")
        print tester.timeit.measured
        assert tester.timeit.measured < 5.0


#-------------------------------------------------------
# This test runs firefox and waits (at most) 10 seconds
# for a specific pattern (regular expression) to appear
# in syslog. 

def test2(tester):
    with tester.device("MedfieldB60440E1") as device:
        with tester.timeout(10):
            device.linux.cmd("firefox")
            device.linux.syslog.wait(".*bla.*")


test1(tester)
#test2(tester)
