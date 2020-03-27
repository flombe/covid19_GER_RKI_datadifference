#!/bin/env python
import os
import logging
from datasetdownloader import DatasetDownloader
from datasetmanglerjhu import DatasetManglerJHU
from datasetmanglerrki import DatasetManglerRKI
from datasetmerger import DatasetMerger
from datasetplotter import DatasetPlotter


logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)
logger = logging.getLogger("main")

JHU_CSSE_REPO = "https://github.com/CSSEGISandData/COVID-19/archive/master.zip"
RKI_REPO = "https://github.com/micgro42/COVID-19-DE/archive/master.zip"
'''
try:
    data = DatasetDownloader()
    data.downloadGitTarball(JHU_CSSE_REPO)
    data.unzipTarball()

    mangler = DatasetManglerJHU(data.getExtractedDir())
    mangler.mangleData()
    mangler.saveData(os.path.join(os.getcwd(), 'data_JHU.csv'))
except Exception:
    logger.exception("Fatal Script Error")

# RKI DATA
try:
    data = DatasetDownloader()
    data.downloadGitTarball(RKI_REPO)
    data.unzipTarball()

    mangler = DatasetManglerRKI(data.getExtractedDir())
    mangler.mangleData()
    mangler.saveData(os.path.join(os.getcwd(), 'data_RKI.csv'))
except Exception:
    logger.exception("Fatal Script Error")

# get final Data in right format
try:
    formater = DatasetMerger()
    formater.formatData()
    formater.saveData(os.path.join(os.getcwd(), 'data_final.csv'))
except Exception:
    logger.exception("Fatal Script Error")
'''
# get plot
try:
    plotter = DatasetPlotter(os.path.join(os.getcwd(), 'data_final.csv'))
    plotter.generatePlot(os.path.join(os.getcwd(), 'compare_plot.png'))
except Exception:
    logger.exception("Fatal Script Error")