#!/bin/env python
import os
import logging
import pandas as pd


class DatasetMerger:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetMerger")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        #
        self.dataframes = {
            'JHU': os.path.join(self.cwd,'data_JHU.csv'),
            'RKI': os.path.join(self.cwd,'data_RKI.csv')
            }
        self.dataframe = pd.DataFrame()

    def formatData(self):

        if not os.path.exists(self.dataframes['JHU']):
            raise Exception("dataframe jhu does not exist")
        if not os.path.exists(self.dataframes['RKI']):
            raise Exception("dataframe rki does not exist")

        jhu = pd.read_csv(self.dataframes['JHU'])
        rki = pd.read_csv(self.dataframes['RKI'])

        rki = rki.transpose()
        rki = rki.rename(columns={0: "RKI_Cases", 1: "RKI_Deaths"})
        rki = rki.drop(rki.index[0])

        jhu = jhu.drop([1]) # drop 'Recovered' since no data for RKI
        jhu = jhu.transpose()
        jhu = jhu.rename(columns={0: "JHU_Cases", 2: "JHU_Deaths"})
        jhu = jhu.drop(jhu.index[0:43])  # hacked...

        # check for df row len (days entered), due to different update cycle of datasources
        while (len(rki.index) != len(jhu.index)):
            self.logger.info("DatasetMerger: Different data progression - drop newest entry that is advanced")
            if len(rki.index) > len(jhu.index):
                rki = rki.drop(rki.index[len(rki.index) - 1])
            else:
                jhu = jhu.drop(jhu.index[len(jhu.index) - 1])

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

    m = DatasetMerger()
    m.formatData()
    m.saveData(os.path.join(os.getcwd(), 'data_final.csv'))