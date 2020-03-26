#!/bin/env python
import os
import logging
import pandas as pd
import matplotlib.pyplot as plt

class DatasetPlotter:

    def __init__(self, workDir=None):
        self.logger = logging.getLogger("DatasetPlotter")
        self.cwd = os.path.abspath(os.getcwd()) if not workDir else os.path.abspath(workDir)

    def plotData(self):
        self.logger.debug("Plot dataset: %s", self)

        if not os.path.exists(self):
            raise Exception("dataset does not exist")

        df  = pd.read_csv(self, index_col=0) # read "data_final.csv
        ax1 = df[["RKI_Cases", "JHU_Cases"]]
        ax2 = df[["RKI_Deaths", "JHU_Deaths"]]

        fig, axarr = plt.subplots(2, figsize=(14, 9), sharex=True)

        ax1.plot.bar(ax=axarr[0], fontsize=11, edgecolor='black')
        ax2.plot.bar(ax=axarr[1], fontsize=11, color=["steelblue", 'peru'], edgecolor='black')

        plt.subplots_adjust(wspace=0, hspace=0.05)

        plt.figtext(.5, .9, 'Vergleich von RKI und JHU', fontsize=20, ha='center')

        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        plt.text(8.5, 150, "Erkrankte", size=18,
                 ha="center", va="center",
                 bbox=bbox_props)

        plt.text(8.5, 55, "Todesfälle", size=18,
                 ha="center", va="center",
                 bbox=bbox_props)

        # plt.savefig('compare_plot.png', bbox_inches="tight")
        # plt.close()


    def savePlot(self, filePath):
        self.logger.info("Save Plot: %s", filePath)
        self.savefig(filePath, bbox_inches="tight")


if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s:%(name)s:%(levelname)s]-> %(message)s', level=logging.DEBUG)

    m = DatasetPlotter()
    m.plotData()
    m.savePlot(os.path.join(os.getcwd(), 'compare_plot.png'))

