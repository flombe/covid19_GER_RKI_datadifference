#!/bin/env python
import os
import logging
from datasetdownloader import DatasetDownloader
from datasetmangler import DatasetMangler

logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)
logger = logging.getLogger("main")

JHU_CSSE_REPO = "https://github.com/CSSEGISandData/COVID-19/archive/master.zip"

try:
    data = DatasetDownloader()
    data.downloadGitTarball(JHU_CSSE_REPO)
    data.unzipTarball()

    mangler = DatasetMangler(data.getExtractedDir())
    mangler.mangleData()
    mangler.saveData(os.path.join(os.getcwd(), 'data.csv'))
except Exception:
    logger.exception("Fatal Script Error")
