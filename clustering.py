from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

class clustering:

    # builds the model of the clustering
    def kmeans(self,data,numOfClustering,numOfRuns):
        x = int(numOfClustering)
        y = int(numOfRuns)
        withoutCountries = pd.DataFrame(data)
        withoutCountries.drop('country',1,inplace=True)
        withoutCountries.drop('year',1,inplace=True)
        fitModel= KMeans(n_clusters=x,init='random',n_init=y).fit_predict(withoutCountries)
        countries = pd.DataFrame(data)
        countries.drop('year',1,inplace=True)
        unionData = countries.assign(clusters=fitModel)
        return unionData