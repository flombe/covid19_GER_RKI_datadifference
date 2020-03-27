#!/bin/env python
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

class DatasetPlotter:

    def __init__(self, filepath, workDir=None):
        self.logger = logging.getLogger("DatasetPlotter")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)
        self.dataframe = filepath

    def generatePlot(self, filePath):
        self.logger.debug("Plot dataset: %s", self.dataframe)

        if not os.path.exists(self.dataframe):
            raise Exception("dataset does not exist %s", self.dataframe)

        df  = pd.read_csv(self.dataframe, index_col=0) # read "data_final.csv
        ax1 = df[["RKI_Cases", "JHU_Cases"]]
        ax2 = df[["RKI_Deaths", "JHU_Deaths"]]

        fig, axarr = plt.subplots(2, figsize=(14, 9), sharex=True)

        ax1.plot.bar(ax=axarr[0], fontsize=11, edgecolor='black')
        ax2.plot.bar(ax=axarr[1], fontsize=11, color=["steelblue", 'peru'], edgecolor='black')

        plt.subplots_adjust(wspace=0, hspace=0.05)

        plt.figtext(.5, .9, 'Vergleich von RKI und JHU', fontsize=20, ha='center')

        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        plt.text(8.5, 470, "Erkrankte", size=18,
                 ha="center", va="center",
                 bbox=bbox_props)

        plt.text(8.5, 180, "Todesfälle", size=18,
                 ha="center", va="center",
                 bbox=bbox_props)

        self.logger.info("Save Plot: %s", os.path.abspath(filePath))
        plt.savefig(os.path.abspath(filePath), bbox_inches="tight")


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    m = DatasetPlotter(os.path.join(os.getcwd(), 'data_final.csv'))
    m.generatePlot(os.path.join(os.getcwd(), 'compare_plot.png'))

