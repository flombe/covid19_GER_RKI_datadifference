#!/bin/env python
import os
import shutil
import logging
import requests
import zipfile

class DatasetDownloader:

    def __init__(self):
        self.logger = logging.getLogger("DatasetDownloader")
        self.cwd = os.path.abspath(os.getcwd())
        self.fileName = None

    def downloadGitTarball(self, url):
        self.logger.info("download: %s", url)
        try:
            r = requests.get(url, allow_redirects=True)
            self.fileName = os.path.join(self.cwd, url.split("/")[-1])
            self.logger.info("save as: %s", self.fileName)
            open(self.fileName, 'wb').write(r.content)
        except Exception:
            self.logger.exception()

    def unzipTarball(self):
        self.logger.info("Unzip tarball to %s", self.cwd)
        if not self.fileName:
            raise Exception("No fileName defined")
        with zipfile.ZipFile(self.fileName, 'r') as zip_ref:
            zip_ref.extractall(self.cwd)
        # delete useless master.zip file
        try:
            os.remove(self.fileName)
            self.fileName = None
        except OSError:
            self.logger.exception()

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    # test data
    JHU_CSSE_REPO = "https://github.com/CSSEGISandData/COVID-19/archive/master.zip"

    data = DatasetDownloader()
    data.downloadGitTarball(JHU_CSSE_REPO)
    data.unzipTarball()
