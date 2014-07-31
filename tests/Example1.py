from infrastructure.BaseTest import BaseTest
import slash

class Example1(BaseTest):
    def test_limit_linux_cpu(self):
        result = None
        with self.tester.timeout(120):
            with self.tester.timeit.measure():
                with self.linux.vitals.measure():
                    self.linux.cmd("libreoffice")
                    result = self.linux.ui.ldtp.waittillguiexist("LibreOffice")
            slash.should.be(self.linux.vitals.measured.cpu.max < 0.6, True)
        slash.should.equal(result, 1)
