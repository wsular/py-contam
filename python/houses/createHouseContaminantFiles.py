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

houses     = ['h002_summer', 'h002_winter', 'h003_summer', 'h003_winter', 'h004_summer', 'h004_winter', 'h005_summer', 'h006_summer', 'h006_winter', 'h007_summer', 'h007_winter', 'h008_summer', 'h008_winter', 'h009_summer', 'h009_winter', 'h010_summer', 'h010_winter']
years      = [2015, 2016, 2015, 2016, 2016, 2017, 2016, 2016, 2017, 2016, 2017, 2018, 2018, 2017, 2018, 2017, 2018]
skiprows   = [32, 24, 15, 13, 17, 14, 18, 13, 14, 20, 14, 17, 21, 14, 14, 15, 16]
elevations = [716.9, 716.9, 716.9, 716.9, 716.9, 716.9, 117.0, 716.9, 716.9, 716.9, 716.9, 716.9, 716.9, 601.1, 601.1, 601.1, 601.1]
det_limit  = [  0.5,   0.5,   0.5,   0.5,   0.5,  0.5,   0.5,    0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5,   0.5]
df         = pd.DataFrame({'year': years, 'skiprows': skiprows, 'directory': ds, 'elevation': elevations, 'detection_limit': det_limit}, index=houses)

for row in df.index:
    house = df.loc[row]
    print('Processing: ', house.name)
    
    #............................... Weather .....................................
    # ....Read weather data
    wth = pd.read_csv('/Users/vonw/data/iaq/houses/weatherFiles/' + 'H' + house.name[1:] + '.wth', 
                      sep='\t', 
                      skiprows=house.skiprows, 
                      header=None, 
                      names=['date', 'time', 'Ta', 'Pb', 'Ws', 'Wd', 'Hr', 'Ith', 'Idn', 'Ts', 'Rn', 'Sn'])
    dates           = wth['date'].str.split('/', expand=True)
    times           = wth['time'].str.split(':', expand=True)
    wth['year']     = house.year
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
    hm  = house.elevation
    wth['Pb']  = wth['Pb'].astype('float') * ( ( 288. - 0.0065*hm) / 288. ) ** 5.2561
    # ....Calculate air density
    wth['density'] = wth['Pb'] / (287. * wth['Ta'].astype('float'))   # 287 is the gas constant for air in J/(kg K).
     
    #............................ Contaminants ...................................
    # ....Read contaminant data
    rack, pm25, ptrms = contam.readHouseContaminantData(house.directory)
    pm25 = pm25.drop(columns=['Unnamed: 2_level_0', 'Unnamed: 3_level_0', 'Unnamed: 4_level_0'])
    
    time_min = max([min(wth.index), min(rack.index), min(pm25.index), min(ptrms.index)])
    time_max = min([max(wth.index), max(rack.index), max(pm25.index), max(ptrms.index)])
    
    # !!!! SPECIAL CASES... (indexing problem...)
    # H008_summer
    if house.name == 'h008_summer':
        time_min = '2018-08-01 09:34:46'
        time_max = '2018-08-10 09:00:00'
    # H009_summer
    if house.name == 'h009_summer':
        time_min = pd.Timestamp('2017-09-08 19:01:00')
    
    wth   = wth[time_min:time_max]
    rack  = rack[time_min:time_max].resample('30T').mean().interpolate()
    pm25  = pm25[time_min:time_max].resample('30T').mean().interpolate()
    ptrms = ptrms[time_min:time_max].resample('30T').mean().interpolate()
    ctm   = pd.concat([rack[1:], pm25[1:], ptrms[1:]], axis=1)
    ctm.columns.names = ['variable', 'units']
    
    # ....Ensures that the weather data are floating-point numbers, not strings; Excel...
    for c in wth.columns:
        if( (c=='Ta') or (c=='Pb') or (c=='Ws') or (c=='Wd') or (c=='Hr') or (c=='Ith') or (c=='Idn') or (c=='Ts') or (c=='Rn') or (c=='Sn') ):
            if( type(wth[c]) != 'float'):
                wth[c] = wth[c].astype('float')
    
    # ....Ensures non-zero values of Formaldehyde when measurements are within
    #     the detection limit of the PTR-MS.
    HCHO = ctm.Formaldehyde.values.flatten()
    HCHO[HCHO < house.detection_limit] = house.detection_limit/2.
    ctm['Formaldehyde'] = HCHO
    
    # ....Unit conversions to (kg of gas) / (kg of air) for contam
    #     Assume that air is dry, which only makes an error < 1%.
    for v, u in ctm.columns:
        # Formaldehyde
        if (v == 'Formaldehyde'):
            if   (u == 'ppm') or (u == 'ppmv'):
                ctm[v] = ctm[v] * (48.00/28.97) / 1e6
            elif (u == 'ppb') or (u == 'ppbv'):
                ctm[v] = ctm[v] * (48.00/28.97) / 1e9
            else:
                pass
        # Ozone
        if (v == 'O3'):
            if   (u == 'ppm') or (u == 'ppmv'):
                ctm[v] = ctm[v] * (30.031/28.97) / 1e6
            elif (u == 'ppb') or (u == 'ppbv'):
                ctm[v] = ctm[v] * (30.031/28.97) / 1e9
            else:
                pass
        # PM2.5
        if (v == 'PM2.5'):
            if u == 'ug/m3':
                ctm[v] = ctm[v].values / (wth['density'].values * 1e9)
            else:
                pass
    
    # ....Write weather and contaminant files to contam simulations.
    #     Weather file
    contam.writeContamWeatherFile(house.directory + house.name[:4] + '_outdoor' + house.name[4:] + '.wth', wth)
    #     Contaminant file
    ctm.columns = ctm.columns.droplevel(1) # drop level 1 of columns so that df works with write function.
    contam.writeContamSpeciesFile(house.directory + house.name[:4] + '_outdoor' + house.name[4:] + '.ctm', ctm[['Formaldehyde', 'O3', 'PM2.5']])
