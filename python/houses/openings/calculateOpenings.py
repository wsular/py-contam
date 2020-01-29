#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:25:08 2019

@author:    Von P. Walden
            Washington State University
"""

#%%
from glob import glob
import pandas as pd
import numpy  as np

# ---- NECESSARY USER INPUT ----
d = '/Users/vonw/data/iaq/houses/SmartHome/YiBo_UTC_WD_CleanedJitter/Atmo5S/'
# validSensors = ['DoorB', 'DoorC', 'DoorD', 'MainDoor']
# ------------------------------

fns = glob(d + '*.txt')
fna = glob(d + 'atmo*.csv')[0]

#%%
# Read all data files for house openings
openings = []
houses = pd.read_csv('/Users/vonw/work/software/iaq/py-contam/python/houses/openings/houseDates.csv', parse_dates=['StartDate','EndDate'])
data   = {}
for fn in fns:
    print(fn)
    opening = fn.split('/')[-1].split('.')[0]
    openings.append(opening)
    df = pd.read_csv(fn, sep='\t', names=['time', 'opening', 'state'], parse_dates=[0])
    # ....Sets up the time index
    df.index = df.time
    df.drop(columns=['time', 'opening'], inplace=True)
    df = df.sort_index()
    # ....Converts True and False to numerical values
    df['state'].loc[df['state']=='CLOSE'] = 0
    df['state'].loc[df['state']=='OPEN']  = 1
    # ....Upsamples the data to 1 second intervals, then downsamples to 30 minutes.
    opening = opening.replace('Temperature','')
    opening = opening.replace('Bathroom','Bath')
    opening = opening.replace('Bedroom','Bed')
    opening = opening.replace('Kitchen','Kit')
    opening = opening.replace('Office','Off')
    opening = opening.replace('LivingRoom','Liv')
    data[opening] = df.resample('1S').ffill().resample('30min').mean()
    # data[opening].to_csv(d+opening+'.csv')

# %%
# Now add the data for all the temperature sensors
print(fna)
atmo = pd.read_csv(fna, parse_dates=[0, 1], names=['time', 'location', 'Temperature'])
atmo.index = atmo.time
sensors = atmo.location.unique()
for sensor in sensors:
    if(sensor.strip() in openings):
        sensorName = sensor.replace('Temperature','')
        sensorName = sensorName.replace('Bathroom','Bath')
        sensorName = sensorName.replace('Bedroom','Bed')
        sensorName = sensorName.replace('Kitchen','Kit')
        sensorName = sensorName.replace('Office','Off')
        sensorName = sensorName.replace('LivingRoom','Liv')
        data['T_' + sensorName.rstrip()] = (atmo[atmo.location == sensor].Temperature+273.15).resample('1S').ffill().resample('30min').mean()

#%%
# Determine the time scale
minTime = np.array([data[key].index[0] for key in data]).max()
minDate = minTime.date()
maxTime = np.array([data[key].index[-1] for key in data]).min()
maxDate = maxTime.date() + pd.Timedelta('1d')   # Add day to get ALL values of the last day.

#%%
#newIndex = pd.date_range(minDate, maxDate, freq='30T')
newIndex = pd.date_range(minTime, maxTime, freq='30T')
data     = pd.concat(data, axis=1)[minTime:maxTime]
# Perpetuates the state of the opening at the beginning and ending of the time series
data     = data.reindex(newIndex, method='nearest')
# data.to_csv(d+'openings.csv')

#%%
# ....Open and write to a contam CVF file
f = open(d+'SmartHomesData.cvf','w')

# Write CVF file
f.write('ContinuousValuesFile ContamW 2.1\n')
f.write('\n')  # blank
f.write(minTime.date().strftime('%m/%d') +'\t' + maxTime.date().strftime('%m/%d') + '\n')
f.write(str(len(data.columns))+'\n')
for opening in data:
    f.write(opening[0]+'\n')
for dataRow in data.iterrows():
    f.write(dataRow[0].strftime('%m/%d') + '\t' + dataRow[0].strftime('%H:%M:%S'))
    for v in dataRow[1]:
        f.write('\t' + "%6.4f" % v)
    f.write('\n')
f.close()
