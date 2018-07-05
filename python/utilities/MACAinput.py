# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 12:42:28 2018

@author: Von P. Walden, Washington State University
"""

import pandas as pd
from contam_input import readMACA, writeContamWeatherFile

d = '/Volumes/vonw/data/iaq/maca/'
cities = pd.read_csv(d + 'iaq_cities.csv')

city   = cities.iloc[0]
year   = 2010
rcp    = 8.5
model  = 'CNRM-CM5'
wth = readMACA(city,year,rcp,model)

writeContamWeatherFile('/Users/vonw/Desktop/' + city.city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth', wth)
