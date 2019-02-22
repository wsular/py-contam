# -*- coding: utf-8 -*-
"""
Created on Thu Aug 31 14:10:45 2017

@author: Von P. Walden, Washington State University
"""

# NOTE to use this script, one must mount /data/hydro_lar/maca_v2_metdata as /Volumes/maca.

import pandas      as     pd
from   maca_aeolus import maca

# Base directory for IAQ data.
d          = '/Volumes/sdata/data/iaq/maca/'
# Open the file containing the list of cities.
cities        = pd.read_csv('/Users/vonw/work/software/iaq/py-contam/python/iaq_cities.csv')

fvar          = ['pr','tasmin','tasmax','uas','vas','huss']
#models        = ['CCSM4','CNRM-CM5','GFDL-ESM2M','HadGEM2-ES365','IPSL-CM5A-LR','MIROC-ESM','MIROC5','NorESM1-M']
# NEED TO DOWNLOAD HUSS FILE FOR NOR-ESM1-M MODEL.
models        = ['CCSM4','CNRM-CM5','GFDL-ESM2M','HadGEM2-ES365','IPSL-CM5A-LR','MIROC-ESM','MIROC5']
# Beginning and ending dates for various decades.
#1990s
#beginningDate = '1995-12-31'
#endingDate    = '2006-01-02'
#2010s
#beginningDate = '2009-12-31'
#endingDate    = '2020-01-02'
#2030s
#beginningDate = '2029-12-31'
#endingDate    = '2040-01-02'
#2040s-2050s
#beginningDate = '2044-12-31'
#endingDate    = '2056-01-02'
#2090s
beginningDate = '2085-12-31'
endingDate    = '2096-01-02'
#beginningDate = '2089-12-31'
#endingDate    = '2099-01-02'


for city in cities.city:
    # Determine coordinates of desired IAQ city.
    lat    = cities.latitude[cities['city']==city].values[0]
    lon    = 360. + cities.longitude[cities['city']==city].values[0]
    #print(lat,lon)
    
    rcp  = 4.5
    for var in fvar:
        data = maca(var,models,rcp,beginningDate,endingDate,lat,lon)
        data.to_csv(d + city.replace(' ','') + '_' + var + '_' + str(rcp) + '_' + beginningDate[0:4] + '_' + endingDate[0:4] + '.csv')

    rcp  = 8.5
    for var in fvar:
        data = maca(var,models,rcp,beginningDate,endingDate,lat,lon)
        data.to_csv(d + city.replace(' ','') + '_' + var + '_' + str(rcp) + '_' + beginningDate[0:4] + '_' + endingDate[0:4] + '.csv')
