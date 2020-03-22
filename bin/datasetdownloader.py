#!/bin/env python
import os
import shutil
import logging
import requests
import zipfile

class DatasetDownloader:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetDownloader")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        self.fileName = None
        self.extractedDirName = None

    def downloadGitTarball(self, url):
        self.logger.info("download: %s", url)
        try:
            r = requests.get(url, allow_redirects=True)
            self.fileName = os.path.join(self.cwd, url.split("/")[-1])
            self.logger.info("save as: %s", self.fileName)
            open(self.fileName, 'wb').write(r.content)
        except Exception:
            self.logger.exception("Cannot download file")

    def unzipTarball(self):
        self.logger.info("Unzip tarball to %s", self.cwd)
        if not self.fileName:
            raise Exception("No fileName defined")
        with zipfile.ZipFile(self.fileName, 'r') as zip_ref:
            self.extractedDirName = zip_ref.namelist()[0]
            zip_ref.extractall(self.cwd)
        self.logger.info("Extracted directory: %s", self.extractedDirName)
        # delete useless master.zip file
        try:
            os.remove(self.fileName)
            self.fileName = None
        except OSError:
            self.logger.exception("Cannot delete file")

    def getExtractedDir(self):
        return os.path.join(self.cwd, self.extractedDirName)

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    # test data
    JHU_CSSE_REPO = "https://github.com/CSSEGISandData/COVID-19/archive/master.zip"

    data = DatasetDownloader()
    data.downloadGitTarball(JHU_CSSE_REPO)
    data.unzipTarball()
