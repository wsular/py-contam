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

def leap_year(year):
    if (( year%400 == 0)or (( year%4 == 0 ) and ( year%100 != 0))):
        return True
    else:
        return False

hostname = gethostname()
if hostname.rfind('gaia')>=0:
    d = '/home/lima/data/iaq/test_homes_modeling/no_opening/'
elif hostname.rfind('nuia')>=0:
    d = '/Users/vonw/data/iaq/test_homes_modeling/no_opening/'
elif hostname.rfind('sila')>=0:
    d = '/Users/vonw/data/iaq/test_homes_modeling/no_opening/'
else:
    d = 'D:/Documents/Lab/CONTAM_modeling/test_homes_modeling/no_opening/'
    
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
nodes = ['Cnd1',
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

for house, year, node in zip(houses, years, nodes):
    # Determine time difference to add to time index to convert times to actual dates and times.
    if leap_year(year) and ((amb.index[0]-pd.datetime(1900,1,1)).days >= 31+28):
        tdiff = (pd.datetime(year,1,2) - pd.datetime(1900,1,1))    # Effectively add an extra day after leap day
    else:
        tdiff = (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    sim       = contam_output.Contam(d + house + '.sim')
    amb       = sim.readAmbient()
    amb.index = amb.index + tdiff
    T  = amb.Tambt
    W = amb.Ws
    oCtm1 = amb.Ctm1
    oCtm2 = amb.Ctm2
    oCtm3 = amb.Ctm3
    
    ctm       = sim.readContaminantNodes()
    ctm['ctm1'].index = ctm['ctm1'].index + tdiff
    ctm['ctm2'].index = ctm['ctm2'].index + tdiff
    ctm['ctm3'].index = ctm['ctm3'].index + tdiff
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
    # ....Contaminants are stored in alphabetical order by contam
    T = T-273.15  # convert to C
    # Outside
    octm1 = oCtm1 * 1e9 * (28.97/30.03)   # Convert to ppb; HCHO
    octm2 = oCtm2 * 1e9 * (28.97/48.)     # Convert to ppb; O3
    octm3 = oCtm3 * 1e9 * 1.25            # Convert to ug m-3; PM2.5
    # Inside
    ctm1 = ctm1 * 1e9 * (28.97/30.03)     # Convert to ppb; HCHO
    ctm2 = ctm2 * 1e9 * (28.97/48.)       # Convert to ppb; O3
    ctm3 = ctm3 * 1e9 * 1.25              # Convert to ug m-3; PM2.5
    df = pd.DataFrame({'outsideAirTemperature': T.values, 
                       'outsideWindSpeed': W.values, 
                       'airChangesPerHour': ach.values, 
                       'outsideHCHO': oCtm1.values, 
                       'outsideO3': oCtm2.values, 
                       'outsidePM2_5': oCtm3.values, 
                       'insideHCHO': ctm1.values, 
                       'insideO3': ctm2.values, 
                       'insidePM2_5': ctm3.values}, 
                       index=T.index)
    df.index.name = 'time'
    ds = xr.Dataset.from_dataframe(df)
    ds.outsideAirTemperature.attrs    = {'longname': 'Outside Air Temperature', 'units': 'degrees C'}
    ds.outsideWindSpeed.attrs         = {'longname': 'Outside Wind Speed', 'units': 'm s-1'}
    ds.airChangesPerHour.attrs        = {'longname': 'Air Changes per Hour', 'units': 'ach'}
    ds.outsideHCHO.attrs              = {'longname': 'Outside Formaldehyde Concentration', 'units': 'ppb'}
    ds.outsideO3.attrs                = {'longname': 'Outside Ozone Concentration', 'units': 'ppb'}
    ds.outsidePM2_5.attrs             = {'longname': 'Outside Particulate Matter less than 2.5 micrometers', 'units': 'ug m-3'}
    ds.insideHCHO.attrs              = {'longname': 'Inside Formaldehyde Concentration', 'units': 'ppb'}
    ds.insideO3.attrs                = {'longname': 'Inside Ozone Concentration', 'units': 'ppb'}
    ds.insidePM2_5.attrs             = {'longname': 'Inside Particulate Matter less than 2.5 micrometers', 'units': 'ug m-3'}
    
    print('Creating: ', d+house+'.nc')
    ds.to_netcdf(d+house+'.nc')
