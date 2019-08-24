#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 23 14:25:04 2019

@author:    Von P. Walden
            Washington State University
"""

import pandas as pd
import contam_input as contam
from glob import glob

# ....Sets directories
ds = glob('/Users/vonw/data/iaq/houses/outdoors/' + '*.xlsx')
ds.sort()
ds = [d.split('.')[0] + '/' for d in ds]

# ....Read weather data
wth = pd.read_csv('/Users/vonw/data/iaq/houses/weatherFiles/H005_summer.wth', 
                  sep='\t', 
                  skiprows=18, 
                  header=None, 
                  names=['date', 'time', 'Ta', 'Pb', 'Ws', 'Wd', 'Hr', 'Ith', 'Idn', 'Ts', 'Rn', 'Sn'])
dates           = wth['date'].str.split('/', expand=True)
times           = wth['time'].str.split(':', expand=True)
wth['year']     = 2016
wth['month']    = dates[0]
wth['day']      = dates[1]
wth['hour']     = times[0]
wth['minute']   = times[1]
wth['second']   = times[2]
wth.index       = pd.to_datetime(wth[['year', 'month', 'day', 'hour', 'minute', 'second']])

# ....Read contaminant data
#for d in ds:
d  = ds[6]      # House 5
ctm, units = contam.readHouseContaminantData(d)

time_min = max([min(wth.index), min(ctm.loc['rack'].index), min(ctm.loc['pm25'].index), min(ctm.loc['ptrms'].index)])
time_max = min([max(wth.index), max(ctm.loc['rack'].index), max(ctm.loc['pm25'].index), max(ctm.loc['ptrms'].index)])

