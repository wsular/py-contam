#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 10:25:08 2019

@author:    Von P. Walden
            Washington State University
"""

from glob import glob
import pandas as pd
import numpy  as np

from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.plotting import figure

d = '/Users/vonw/data/iaq/houses/SmartHome/YiBo_UTC_WD_CleanedJitter/Atmo5SandW/'
fns = glob(d + '*.txt')

#%%
# Read all data files
houses = pd.read_csv('houseDates.csv', parse_dates=['StartDate','EndDate'])
df = pd.DataFrame(pd.read_csv(fns[0], sep='\t', names=['time', 'opening', 'state'], parse_dates=[0]))
for fn in fns:
    print(fn)
    df = pd.concat([df, pd.read_csv(fn, sep='\t', names=['time', 'opening', 'state'], parse_dates=[0])])
df.index = df.time
df.drop(columns=['time'], inplace=True)
df = df.sort_index()
df['code'] = np.nan
df['code'].loc[df['state']=='CLOSE'] = 0
df['code'].loc[df['state']=='OPEN']  = 1

#%%
doorA = pd.DataFrame({'DoorA':df[df.opening=='DoorA'].code})
doorB = pd.DataFrame({'DoorB':df[df.opening=='DoorB'].code})
doorC = pd.DataFrame({'DoorC':df[df.opening=='DoorC'].code})
doorD = pd.DataFrame({'DoorD':df[df.opening=='DoorD'].code})
doorE = pd.DataFrame({'DoorE':df[df.opening=='DoorE'].code})

openings = doorA.join([doorB, doorC, doorD, doorE], how='outer').ffill()

#%%