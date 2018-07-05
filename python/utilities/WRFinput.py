# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 15:36:24 2017

@author: Von P. Walden, Washington State University
"""
from contam_input import readWRF_CMAQ, writeContamWeatherFile

gridFile = '/Users/vonw/data/iaq/cmaq/GRIDCRO2D_19941215'
dataFile = '/Users/vonw/data/iaq/cmaq/extr/rcp8.5/2040ei_v6_cb05v2_ref_RCP8.5.combine.aconc.2050.01'
lat      = 46.7
lon      = -117.2
 
df       = readWRF_CMAQ(gridFile, dataFile, lat, lon)

wthrFile = '/Users/vonw/data/iaq/cmaq/tmp.wth'

writeContamWeatherFile(wthrFile, df)
