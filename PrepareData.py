import pandas as pd
import numpy as np
import numbers as num

import sklearn.preprocessing
import xlrd
from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, ttk
from tkinter.filedialog import askopenfilename
import statistics as stats


class PrepareData:
    # cleans the data for the model
    def cleanData(self, address, clusters, runs):
        try:
            dataFrame = pd.read_excel(address)
            if not (isinstance(clusters, int) or isinstance(runs,int)):
                return None
            if(dataFrame.empty):
                 return None
            if(clusters<=1 or runs<=0):
                return None
            if(clusters>dataFrame['country'].count()):
                return None

            for column in dataFrame.columns[1:]:
                if np.issubdtype(dataFrame[column].dtype, np.number) and column!= 'year':
                    dataFrame[column].fillna(dataFrame[column].mean(), inplace=True)
                    normalixed_col = ((dataFrame[column]-dataFrame[column].mean())/dataFrame[column].std())
                    dataFrame[column] = normalixed_col
            newDF=dataFrame.groupby(['country'],as_index=False).mean()
            return newDF
        except xlrd.XLRDError:
            return None

