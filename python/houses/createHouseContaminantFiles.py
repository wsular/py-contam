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

#............................ Setup Information ..............................
#  wth file   skiprows year    index
# H002_summer    32    2015    0
# H002_winter    24    2016    1
# 
# H003_summer    15    2015    2
# H003_winter    13    2016    3
# 
# H004_summer    17    2016    4
# H004_winter    14    2017    5
# 
# H005_summer    18    2016    6
#
# H006_summer    13    2016    7
# H006_winter    14    2017    8
# 
# H007_summer    20    2016    9
# H007_winter    14    2017    10
# 
# H008_summer    17    2018    11
# H008_winter    21    2018    12
# 
# H009_summer    14    2017    13
# H009_winter    14    2018    14
# 
# H010_summer    15    2017    15
# H010_winter    16    2018    16

#............................... Weather .....................................
# ....Read weather data
wth = pd.read_csv('/Users/vonw/data/iaq/houses/weatherFiles/H004_summer.wth', 
                  sep='\t', 
                  skiprows=17, 
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

# ....Convert sea-level pressures to station pressure using:
#         https://www.weather.gov/media/epz/wxcalc/stationPressure.pdf
#hm  = 117.         # Richland, WA: House 5
#hm  = 716.9        # Pullman, WA: Houses 2, 3, 4, 6, 7, 8
hm  = 601.1        # Colfax, WA: Houses 9, 10
wth['Pb']  = wth['Pb'].astype('float') * ( ( 288. - 0.0065*hm) / 288. ) ** 5.2561
# ....Calculate air density
wth['density'] = wth['Pb'] / (287. * wth['Ta'].astype('float'))   # 287 is the gas constant for air in J/(kg K).
 
#............................ Contaminants ...................................
# ....Read contaminant data
#for d in ds:
d  = ds[0]      # House
rack, pm25, ptrms = contam.readHouseContaminantData(d)
pm25 = pm25.drop(columns=['Unnamed: 2_level_0', 'Unnamed: 3_level_0', 'Unnamed: 4_level_0'])

time_min = max([min(wth.index), min(rack.index), min(pm25.index), min(ptrms.index)])
time_max = min([max(wth.index), max(rack.index), max(pm25.index), max(ptrms.index)])

# !!!! SPECIAL CASES... (indexing problem...)
# h008_summer
#time_min = '2018-08-01 09:34:46'
#time_max = '2018-08-10 09:00:00'
# h009_summer
#time_min = pd.Timestamp('2017-09-08 19:01:00')

wth   = wth[time_min:time_max]
rack  = rack[time_min:time_max].resample('30T').mean().interpolate()
pm25  = pm25[time_min:time_max].resample('30T').mean().interpolate()
ptrms = ptrms[time_min:time_max].resample('30T').mean().interpolate()
ctm   = pd.concat([rack[1:], pm25[1:], ptrms[1:]], axis=1)

# ....Ensures that the weather data are floating-point numbers, not strings; Excel...
for c in wth.columns:
    if( (c=='Ta') or (c=='Pb') or (c=='Ws') or (c=='Wd') or (c=='Hr') or (c=='Ith') or (c=='Idn') or (c=='Ts') or (c=='Rn') or (c=='Sn') ):
        if( type(wth[c]) != 'float'):
            wth[c] = wth[c].astype('float')

for v, u in ctm.columns:
    if   (u == 'ppm') or (u == 'ppmv'):
        ctm[v] = ctm[v] / 1e6
    elif (u == 'ppb') or (u == 'ppbv'):
        ctm[v] = ctm[v] / 1e9
    elif u == 'ug/m3':
        ctm[v] = ctm[v].values / (wth['density'].values * 1e9)
    else:
        pass

# ....Write weather and contaminant files to contam simulations.
#     Weather file
contam.writeContamWeatherFile(d + d.split('/')[-2] + '.wth', wth)
#     Contaminant file
ctm.columns = ctm.columns.droplevel(1) # drop level 1 of columns so that df works with write function.
contam.writeContamSpeciesFile(d + d.split('/')[-2] + '.ctm', ctm[['O3', 'PM2.5', 'Formaldehyde']])
