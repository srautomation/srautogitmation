import slash
import os
from bunch import Bunch
slash.config.sr = Bunch()

slash.config.sr.paths = Bunch( resources=os.environ.get("SR_RESOURCES", "/tmp/sr/resources")
                             , outputs=os.environ.get("SR_OUTPUTS", "/tmp/sr/outputs")
                             )

slash.config.sr.files = Bunch( pdf="example.pdf"
                             , odt="example.odf"
                             , docx="example.docx"
                             , large="example.large"
                             , jpg="example.jpg"
                             , xlsx="example.xlsx"
                             , ppt="example.ppt"
                             , txt="example.txt"
                             , avi="example.avi"
                             , mp3="example.mp3"
                             , wav="example.wav"
                             , track1="track1.mp3"
                             , track2="track2.mp3"
                             )

slash.config.sr.thresholds = Bunch( cpu_max=0.9
                                  , mem_max=900000000
                                  , bat_max=(0.25*1.05) / 60 # (=0.004375) batt use per sec. (out of 100)
                                  , time_max=9999999999
                                  )
 
