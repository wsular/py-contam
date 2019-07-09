# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:31:07 2019

@author: Von P. Walden, Washington State University
"""
from contam_input import readHouseData

d   = '/Volumes/VONSDRIVE/IAQ archived data/'
fns = ['H002_summer/H002_summer_weather_final.xlsx',
       'H002_winter/H002_winter_Weather_data_final.xlsx',
       'H003_summer/H003_summer_weather_final.xlsx',
       'H003_winter/H003_winter_WeatherStation_final.xlsx',
       'H004_summer/H004_summer_WeatherData_final.xlsx',
       'H004_winter/H004_winter_weather station data_final.xlsx',
       'H005_summer/H005_summer_weather station_final.xlsx',
       'H006_summer/H006_summer_weather station data_final.xlsx',
       'H006_winter/H006_winter_weather station_final.xlsx',
       'H007_summer/H007_summer_weather station data_final.xlsx',
       'H007_winter/H007_winter_weather station data_final.xlsx',
       'H008_summer/H008_summer_weather station data_final.xlsx',
       'H008_winter/H008_winter_weather station data_final.xlsx',
       'H009_summer/H009_summer_weather station data_final.xlsx',
       'H009_winter/H009_winter_weather station data_final.xlsx',
       'H010_summer/H010_summer_weather station data_final.xlsx',
       'H010_winter/H010_winter_weather station data_final.xlsx']

for fn in fns:
    print('Processing:  ', d + fn)
    wth = readHouseData(d + fn)

