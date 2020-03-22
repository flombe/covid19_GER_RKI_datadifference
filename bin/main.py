#!/bin/env python
import logging
from datasetdownloader import DatasetDownloader

logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

JHU_CSSE_REPO = "https://github.com/CSSEGISandData/COVID-19/archive/master.zip"

data = DatasetDownloader()
data.downloadGitTarball(JHU_CSSE_REPO)
data.unzipTarball()
