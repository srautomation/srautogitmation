import slash
import os
from bunch import Bunch
import time
slash.config.sr = Bunch()

slash.config.sr.calendar = Bunch( sender="srusertest@gmail.com"
                            , receivers=["srusertest2@gmail.com"]
                            , name="Test%s"%time.time()
                            , location="Tel Aviv"
                            )
