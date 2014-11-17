from sr_tests.base.BaseTest import BaseTest
import slash
import time

class Example1(BaseTest):
    def test_limit_linux_cpu(self):
        with self.tester.timeout(120):
            with self.device.resources.measure():

                #---------------------------
                # Run Leafpad, measure time
                with self.tester.timeit.measure():
                    self.linux.cmd("leafpad")
                    time.sleep(8)
                    #is_window_visible = self.linux.ui.ldtp.waittillguiexist("(Untitled)")
                    #slash.should.equal(is_window_visible, 1)

                #---------------------------
                # Get Leafpad's TextArea
                leafpad = self.linux.ui.dogtail.tree.root.child("(Untitled)")
                textbox = leafpad.child(roleName = "text")
                textbox.text = "Hello world from automation!"
                time.sleep(5)
                textbox.text = "Leafpad window took %f seconds to show" % self.tester.timeit.measured
                time.sleep(5)

                #---------------------------
                # Press menus to open a file
                textbox.text = "Let's open a file..."                 ; time.sleep(3)
                leafpad.child("File").click()                         ; time.sleep(2)
                leafpad.child("File").child("Open...").click()        ; time.sleep(2)
                self.linux.ui.dogtail.tree.root.child("No").click()   ; time.sleep(2)
                self.linux.ui.dogtail.tree.root.child("root").click() ; time.sleep(2)

                #---------------------------
                # Measure time it takes for file to open
                with self.tester.timeit.measure():
                    self.linux.ui.dogtail.tree.root.child("Example1.py").doubleClick()
                    textbox = leafpad.child(roleName = "text")
                    while not textbox.text.startswith("from sr_automation"):
                        time.sleep(0.01)
                time.sleep(4)

                textbox.text = "File took %f seconds to open" % self.tester.timeit.measured ; time.sleep(4)
                textbox.text = "Bye Bye!" ; time.sleep(7)
                time.sleep(4)

            # Make sure CPU usage was under 60% during test
            slash.should.be(self.device.resources.measured.cpu.max < 0.6, True)
