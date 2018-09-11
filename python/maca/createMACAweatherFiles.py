# -*- coding: utf-8 -*-
"""
Created on Wed Jun 20 12:17:11 2018

@author: Von P. Walden, Washington State University
"""
import sys
import pandas as pd
from contam_input import readMACA, writeContamWeatherFile

from socket import gethostname
hostname = gethostname()
print(hostname)

if hostname.find('sila') >= 0:
    d = '/Volumes/vonw/data/iaq/maca/'
else:
    print('Not a valid computer for access to MACA data. Try again...')
    sys.exit()

years  = range(2010,2019)
#years  = range(2045,2056)
#years  = range(2090,2099)
cities = pd.read_csv(d + 'iaq_cities.csv')
models = ['CCSM4','CNRM-CM5','GFDL-ESM2M','HadGEM2-ES365','IPSL-CM5A-LR','MIROC-ESM','MIROC5']
#model  = 'CNRM-CM5'

for year in years:
    for row, city in cities.iterrows():
        for rcp in ['8.5']:
            for model in models:
                print('Processing: ' + str(year) + ' ' + city.city + ' ' + model + ' ' + rcp)
                wth = readMACA(city,year,rcp,model)
                writeContamWeatherFile('/Volumes/vonw/data/iaq/contam/weatherFiles/' + city.city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth', wth)
