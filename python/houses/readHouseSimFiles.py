#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 13:13:47 2019

@author:    Von P. Walden
            Washington State University
"""
import pandas as pd
import contam_output
from socket import gethostname

hostname = gethostname()
if hostname.rfind('gaia')>=0:
    d = '/mnt/data/lima/iaq/houses/outdoors/'
elif hostname.rfind('nuia')>=0:
    d = '/Users/vonw/data/iaq/houses/test_homes/'
elif hostname.rfind('sila')>=0:
    d = '/Users/vonw/data/iaq/houses/test_homes/'
else:
    d = 'D:\'
    
houses = ['h002_summer',
          'h002_winter',
          'h003_summer',
          'h003_winter',
          'h004_summer',
          'h004_winter',
          'h005_summer',
          'h006_summer',
          'h006_winter',
          'h007_summer',
          'h007_winter',
          'h008_summer',
          'h008_winter',
          'h009_summer',
          'h009_winter',
          'h010_summer',
          'h010_winter']
years  = [2015,
          2016,
          2015,
          2016,
          2016,
          2017,
          2016,
          2016,
          2017,
          2016,
          2017,
          2018,
          2018,
          2017,
          2018,
          2017,
          2018]
node  = ['Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1',
         'Cnd1']

hdf = pd.HDFStore(d+'houses.hdf')

for house, year in zip(houses, years):
    sim       = contam_output.Contam(d + house + '.sim')
    amb       = sim.readAmbient()
    amb.index = amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    T  = amb.Tambt
    W = amb.Ws
    oCtm1 = amb.Ctm1
    oCtm2 = amb.Ctm2
    oCtm3 = amb.Ctm3
    
    ctm       = sim.readContaminantNodes()
    ctm['ctm1'].index = ctm['ctm1'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    ctm['ctm2'].index = ctm['ctm2'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    ctm['ctm3'].index = ctm['ctm3'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    ctm1  = ctm['ctm1'][node]
    ctm2  = ctm['ctm2'][node]
    ctm3  = ctm['ctm3'][node]
    # ACH
    achp  = pd.read_csv(d + house + '.ach', sep='\t', skiprows=1)
    dates = [pd.datetime(year,int(m),int(d)) for m,d in [date.split('/') for date in achp.day]]
    hours = [int(hr[0:2]) for hr in achp.time]
    achp.index = [date + pd.to_timedelta(hour, 'h') for date, hour in zip(dates,hours)]
    ach  = achp.total

    # Unit conversions
    T = T-273.15  # convert to C
    octm1 = oCtm1 * 1e9 * (28.97/30.03)   # Convert to ppb
    octm2 = oCtm2 * 1e9 * (28.97/48.)     # Convert to ppb
    octm3 = oCtm3 * 1e9 * 1.25            # Convert to ug m-3
    ctm1 = ctm1 * 1e9 * (28.97/30.03)     # Convert to ppb
    ctm2 = ctm2 * 1e9 * (28.97/48.)       # Convert to ppb
    ctm3 = ctm3 * 1e9 * 1.25              # Convert to ug m-3
    
    # Save data file.
    hdf.put(house+'/T', T)
    hdf.put(house+'/W', W)
    hdf.put(house+'/octm1', octm1)
    hdf.put(house+'/octm2', octm2)
    hdf.put(house+'/octm3', octm3)
    hdf.put(house+'/ctm1', ctm1)
    hdf.put(house+'/ctm2', ctm2)
    hdf.put(house+'/ctm3', ctm3)
    hdf.put(house+'/ach', ach)

hdf.close()
