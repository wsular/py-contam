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
from shutil import copyfile

# ....Reads in the list of houses and sets the indices of valid houses to process.
houses       = pd.read_csv('/home/vonw/work/software/iaq/py-contam/python/houses/openings/houseDates.csv', parse_dates=['StartDate','EndDate'])
validHouses  = [2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
validSensors = {'Atmo2S': ['RelayA', 'RelayC', 'RelayD', 'RelayB', 'MainDoor', 'DoorC', 'DoorD', 'DoorB', 'KitchenATemperature', 'KitchenAWindowA', 'DoorE', 'OfficeAWindowA', 'BedroomAWindowA', 'BathroomAWindowA', 'BathroomATemperature', 'BathroomBTemperature', 'DoorF', 'BedroomAWindowB'],
                'Atmo2W': ['BedroomAWindowA', 'RelayC', 'BedroomAWindowB', 'BathroomAWindowA', 'BathroomATemperature', 'RelayE', 'RelayB', 'BathroomBTemperature', 'OfficeAWindowA', 'KitchenAWindowA', 'DoorF', 'DoorB', 'RelayD', 'DoorC', 'DoorE', 'MainDoor', 'KitchenATemperature', 'RelayA', 'DoorD'],
                'Atmo4S': ['RelayA', 'RelayB', 'RelayC', 'RelayE', 'RelayD', 'MainDoor', 'DoorC', 'KitchenATemperature', 'BathroomBTemperature', 'BathroomATemperature', 'BedroomBWindowA', 'BathroomAWindowA', 'BedroomAWindowA', 'LivingRoomAWindowA', 'DoorB', 'DoorD', 'DiningRoomAwindowA', 'LivingRoomBWindowA', 'OfficeAwindowA', 'RelayG', 'RelayF', 'BedroomDWindowA', 'BedroomCWindowA', 'RelayH', 'KitchenAWindowA'],
                'Atmo5S': ['RelayA ', 'RelayB ', 'DoorD  ', 'DoorB  ', 'DoorA  ', 'DoorC  ', 'DoorE  '],
                'Atmo6S': ['RelayA', 'RelayB', 'DoorA', 'DoorB', 'DoorC', 'WindowA', 'WindowE', 'WindowC', 'WindowD'],
                'Atmo6W': ['RelayB', 'RelayC', 'KitchenATemperature', 'BathroomATemperature', 'BathroomBTemperature', 'MainDoor', 'RelayA', 'WindowA', 'WindowB', 'WindowC', 'WindowD', 'WindowE', 'DoorB', 'DoorC'],
                'Atmo7S': ['RelayA', 'RelayB', 'DoorA', 'DoorB', 'DoorC', 'KitchenATemperature', 'WindowA', 'BathroomATemperature', 'WindowC', 'WindowD', 'WindowB'],
                'Atmo7W': ['RelayA', 'RelayB', 'DoorA', 'DoorB', 'DoorC', 'KitchenATemperature', 'WindowA', 'BathroomATemperature', 'WindowC', 'WindowD', 'WindowE', 'WindowB', 'RelayC', 'BathroomBTemperature'],
                'Atmo8S': ['RelayA', 'RelayB', 'RelayC', 'RelayD', 'RelayE', 'RelayF', 'RelayG', 'RelayH', 'MainDoor', 'DoorC', 'DoorD', 'DoorB', 'GarageDoor', 'KitchenATemperature', 'BathroomATemperature', 'BathroomBTemperature', 'BathroomCTemperature', 'BathroomDTemperature', 'WindowB', 'WindowA', 'WindowD', 'WindowC', 'WindowG', 'WindowH'],
                'Atmo8W': ['RelayC', 'RelayA', 'RelayB', 'RelayD', 'RelayE', 'RelayF', 'BathroomCTemp', 'DoorD', 'MainDoor', 'DoorB', 'DoorC', 'KitchenATemperature', 'RelayG', 'RelayH', 'BathroomATemperature', 'BathroomBTemperature', 'GarageDoor', 'BathroomDTemp'],
                'Atmo9S': ['WindowC', 'KitchenATemperature', 'BathroomATemperature', 'RelayC', 'RelayD', 'RelayB', 'WindowB', 'BathroomBTemperature', 'DoorB', 'DoorC', 'MainDoor', 'RelayA', 'WindowA', 'BathroomCTemperature'],
                'Atmo9W': ['RelayA', 'BathroomBTemperature', 'RelayC', 'RelayB', 'BathroomCTemperature', 'RelayD', 'RelayE', 'BathroomATemperature', 'DoorB', 'DoorC', 'KitchenATemperature', 'MainDoor', 'RelayF'],
                'Atmo10S': ['RelayD', 'RelayF', 'RelayE', 'RelayA', 'RelayB', 'RelayC', 'WindowC', 'DoorD', 'WindowG', 'BathroomBTemperature', 'WindowF', 'KitchenATemperature', 'WindowI', 'WindowH', 'DoorB', 'MainDoor', 'BathroomCTemperature', 'BathroomATemperature', 'WindowA', 'DoorC', 'WindowB', 'WindowJ', 'WindowK', 'WindowD', 'WindowE'],
                'Atmo10W': ['BathroomBTemperature', 'RelayB', 'RelayE', 'RelayF', 'RelayC', 'RelayA', 'RelayD', 'RelayG', 'MainDoor', 'DoorC', 'DoorD', 'KitchenATemperature', 'DoorB', 'BathroomATemperature', 'BathroomCTemperature']
                } 

# ....Data directory
d = '/home/lima/data/iaq/houses/SmartHome/YiBo_UTC_WD_CleanedJitter/'

# ....Process each valid house
for house in houses.iterrows():
    if house[0] in validHouses:
        houseDir = d + house[1].HouseCode + house[1].Season[0].capitalize() + '/'
        print('\nProcessing: ', houseDir)
        
        fns = glob(houseDir + '*.txt')
        fna = glob(houseDir + 'atmo*.csv')[0]
        
        # ....Read all data files for house openings
        openings = []
        data     = {}
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
            df['state'].loc[df['state']=='CLOSE'] = 0.
            df['state'].loc[df['state']=='OPEN']  = 1.
            df['state'] = df['state'].astype(int)
            # ....Upsamples the data to 1 second intervals, then downsamples to 30 minutes.
            opening = opening.replace('Temperature','')
            opening = opening.replace('Bathroom','Bath')
            opening = opening.replace('Bedroom','Bed')
            opening = opening.replace('Kitchen','Kit')
            opening = opening.replace('Office','Off')
            opening = opening.replace('LivingRoom','Liv')
            opening = opening.replace('DiningRoom','Din')
            data[opening] = df.resample('1S').ffill().resample('30min').mean()
        
        # ....Now add the data for all the temperature sensors
        print(fna)
        atmo = pd.read_csv(fna, parse_dates=[0, 1], names=['time', 'location', 'Temperature'])
        atmo.index = atmo.time
        sensors = atmo.location.unique()
        for sensor in validSensors[houseDir.split('/')[-2]]:
            sensorName = sensor.strip().replace('Temperature','')
            sensorName = sensorName.replace('Bathroom','Bath')
            sensorName = sensorName.replace('Bedroom','Bed')
            sensorName = sensorName.replace('Kitchen','Kit')
            sensorName = sensorName.replace('Office','Off')
            sensorName = sensorName.replace('LivingRoom','Liv')
            sensorName = sensorName.replace('DiningRoom','Din')
            data['T_' + sensorName.rstrip()] = (atmo[atmo.location == sensor].Temperature+273.15).resample('1S').ffill().resample('30min').mean()
        
        # ....Determine the time scale
        minTime = np.array([data[key].index[0] for key in data]).max()
        minDate = minTime.date()
        maxTime = np.array([data[key].index[-1] for key in data]).min()
        maxDate = maxTime.date() + pd.Timedelta('1d')   # Add day to get ALL values of the last day.
        
        #newIndex = pd.date_range(minDate, maxDate, freq='30T')
        newIndex = pd.date_range(minTime, maxTime, freq='30T')
        data     = pd.concat(data, axis=1)[minTime:maxTime]
        # Perpetuates the state of the opening at the beginning and ending of the time series
        data     = data.reindex(newIndex, method='nearest')
        # data.to_csv(d+'openings.csv')
        
        # ....Open and write to a contam CVF file
        f = open(houseDir + 'SmartHomesData.cvf','w')
        
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
        
        # ....Make a copy of the file in a separate directory
        copyfile(houseDir + 'SmartHomesData.cvf', '/home/vonw/data/iaq/houses/SmartHome/CVF_files/' + houseDir.split('/')[-2] + '_SmartHomesData.cvf')
