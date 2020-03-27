#!/bin/env python
import os
import logging
import pandas as pd


class DatasetManglerRKI:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetManglerRKI")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        #
        self.datasets = {
            'confirmed': os.path.join(self.cwd,'time_series/time-series_19-covid-Confirmed.csv'),
            'deaths': os.path.join(self.cwd,'time_series/time-series_19-covid-Deaths.csv')
            }
        self.dataframe = pd.DataFrame()

    def mangleData(self):
        for key in self.datasets.keys():
            self.logger.debug("Mangle dataset: %s", self.datasets[key])

            if not os.path.exists(self.datasets[key]):
                raise Exception("dataset does not exist")

            df = pd.read_csv(self.datasets[key])
            df = df.sum(axis=0).to_frame(name=key)  # to transform to dataframe not series
            df = df.transpose()

            self.dataframe = self.dataframe.append(df)

        self.dataframe = self.dataframe.rename(columns={"State": "Source"})
        self.dataframe["Source"] = "RKI"
        #### Type (confirmed, deaths) is row index not first column compared to JHU data

    def saveData(self, filePath):
        self.logger.info("Save data: %s", filePath)
        self.dataframe.to_csv(filePath, encoding='utf-8', index=False)


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    m = DatasetMangler()
    m.mangleData()
    m.saveData(os.path.join(os.getcwd(), 'data_RKI.csv'))