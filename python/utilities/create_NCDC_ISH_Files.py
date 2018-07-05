# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 09:36:49 2017

@author: Von P. Walden, Washington State University
"""

from contam_input import readNOAA_ISH, writeContamWeatherFile
import pandas as pd
import numpy  as np

stations = pd.read_csv('/Volumes/vonw/data/iaq/NCDC/ish/isd-history-IAQ.csv')

for station in stations.itertuples():
    print(station.CITY)
    for year in np.arange(2004,2014):
        print(year)
        if ((station.CITY=='Worcester') and (year<2010)): continue
        df = readNOAA_ISH(str(station.USAF), str(station.WBAN), year)
        writeContamWeatherFile('/Volumes/vonw/data/iaq/contam/weatherFiles/'+station.CITY+'_'+str(year)+'.wth', df)

