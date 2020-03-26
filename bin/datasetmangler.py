#!/bin/env python
import os
import logging
import pandas as pd

class DatasetMangler:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetMangler")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        #
        self.datasets = {
            'confirmed': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'),
            'recovered': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'),
            'deaths': os.path.join(self.cwd,'csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
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



### copy of DatasetMangler

class DatasetMangler2:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetMangler")
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


### copy of DatasetMangler - to combine both dataframes

class DatasetFormater:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetFormater")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        #
        self.dataframes = {
            'JHU': os.path.join(self.cwd,'data_JHU.csv'),  ## to fix
            'RKI': os.path.join(self.cwd,'data_RKI.csv')
            }
        self.dataframe = pd.DataFrame()

    def formatData(self):
        ### fix

        jhu = pd.read_csv(self.dataframes['JHU'])
        rki = pd.read_csv(self.dataframes['RKI'])

        rki = rki.transpose()
        rki = rki.rename(columns={"Confirmed": "RKI_Cases", "Deaths": "RKI_Deaths"})
        rki = rki.drop(rki.index[0])

        jhu = jhu.drop([1]) # drop 'Recovered' since no data for RKI
        jhu = jhu.transpose()
        jhu = jhu.rename(columns={0: "JHU_Cases", 2: "JHU_Deaths"})
        jhu = jhu.drop(jhu.index[0:43])  # hacked...
        jhu.index = rki.index
        # better option(?): to cast indices and intersect
        # x = pd.to_datetime(jhu.columns[2:])
        # y = pd.to_datetime(df.columns[1:])
        # xy, x_ind, y_ind = np.intersect1d(x, y, return_indices=True)

        rki[["JHU_Cases", "JHU_Deaths"]] = jhu[["JHU_Cases", "JHU_Deaths"]]  # add JHU columns

        # calculate Delta rows
        delta_1 = rki["RKI_Cases"] - rki["JHU_Cases"]
        rki["Delta_Cases"] = delta_1

        delta_2 = rki["RKI_Deaths"] - rki["JHU_Deaths"]
        rki["Delta_Deaths"] = delta_2

        self.dataframe = rki


    def saveData(self, filePath):
        self.logger.info("Save data: %s", filePath)
        self.dataframe.to_csv(filePath, encoding='utf-8', index=True) # index true to keep dates


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    m = DatasetFormater()
    m.formatData()
    m.saveData(os.path.join(os.getcwd(), 'data_final.csv'))