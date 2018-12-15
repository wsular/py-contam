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

if hostname.find('petb227a') >= 0:    # This is the hostname for gaia.
    in_d  = '/mnt/data/lima/iaq/maca/'
    out_d = '/mnt/data/lima/iaq/contam/weatherFiles/'
elif hostname.find('sila') >= 0:
    in_d  = '/Volumes/vonw/data/iaq/maca/'
    out_d = '/Volumes/vonw/data/iaq/contam/weatherFiles/'
else:
    print('Not a valid computer for access to MACA data. Try again...')
    sys.exit()

rcps   = ['4.5', '8.5']
#rcps   = ['8.5']
#years  = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]
years  = [2048, 2052]   # leap years
#years  = [2045, 2046, 2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054]
#years  = [2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098]
#years  = [2092, 2096]   # leap years

cities = pd.read_csv(in_d + 'iaq_cities.csv')
models = ['CCSM4','CNRM-CM5','GFDL-ESM2M','HadGEM2-ES365','IPSL-CM5A-LR','MIROC-ESM','MIROC5']
#model  = 'CNRM-CM5'

for year in years:
    for row, city in cities.iterrows():
        for rcp in rcps:
            for model in models:
                print('Processing: ' + str(year) + ' ' + city.city + ' ' + model + ' ' + rcp)
                wth = readMACA(city,year,rcp,model)
                writeContamWeatherFile(out_d + city.city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth', wth)
