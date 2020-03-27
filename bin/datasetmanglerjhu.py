#!/bin/env python
import os
import logging
import pandas as pd

class DatasetManglerJHU:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetManglerJHU")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        #
        self.datasets = {
            'confirmed': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'),
            'recovered': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'),
            'deaths': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
            }
        self.dataframe = pd.DataFrame()

    def mangleData(self):
        for key in self.datasets.keys():
            self.logger.debug("Mangle dataset: %s", self.datasets[key])

            if not os.path.exists(self.datasets[key]):
                raise Exception("dataset does not exist")

            df  = pd.read_csv(self.datasets[key])
            self.dataframe = self.dataframe.append(df[ df["Country/Region"] == "Germany" ])

        self.dataframe.columns.values[0] = 'Type'
        self.dataframe = self.dataframe.assign(Type = ("Confirmed", "Recovered", "Deaths"))
        self.dataframe = self.dataframe.drop(['Lat', 'Long'], 1)

    def saveData(self, filePath):
        self.logger.info("Save data: %s", filePath)
        self.dataframe.to_csv(filePath, encoding='utf-8', index=False)


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    m = DatasetMangler()
    m.mangleData()
    m.saveData(os.path.join(os.getcwd(), 'data_JHU.csv'))
