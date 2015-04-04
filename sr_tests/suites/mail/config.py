import slash
import os
from bunch import Bunch
slash.config.sr = Bunch()

slash.config.sr.paths = Bunch( resources=os.environ.get("SR_RESOURCES", "/tmp/resources")
                             )

slash.config.sr.files = Bunch( pdf="example.pdf"
                             , docx="example.docx"
                             , large="large.file"
                             , picture="example.jpg"
                             , langs="example.txt"
                             )

slash.config.sr.mail = Bunch( sender="intel.elad1@gmail.com"
                            , receivers=["barak@wizery.com"]
                            , subject="subject"
                            , body="body"
                            , inlinepic='<img src="{}">'.format(slash.config.sr.files.picture)
                            , link='<a href="www.google.com">Google</a>'
                            )
