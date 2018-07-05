# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:25:27 2018

@author: Von P. Walden, Washington State University
"""
#%%
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt

d = '/Volumes/vonw/data/iaq/maca/'

cities = pd.read_csv(d + 'iaq_cities.csv')

#%% Tmax
for city in cities.iterrows():
    Tmax_rcp45_2010 = pd.read_csv(d + city[1].city + '_tasmax_4.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmax_rcp45_2050 = pd.read_csv(d + city[1].city + '_tasmax_4.5_2044_2056.csv', index_col='time', parse_dates=True)
    Tmax_rcp85_2010 = pd.read_csv(d + city[1].city + '_tasmax_8.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmax_rcp85_2050 = pd.read_csv(d + city[1].city + '_tasmax_8.5_2044_2056.csv', index_col='time', parse_dates=True)
    
    Tmin = np.min([Tmax_rcp45_2010.min().min(),
                Tmax_rcp85_2010.min().min(),
                Tmax_rcp45_2050.min().min(),
                Tmax_rcp85_2050.min().min()]) - 273.15
    Tmax = np.min([Tmax_rcp45_2010.max().max(),
                Tmax_rcp85_2010.max().max(),
                Tmax_rcp45_2050.max().max(),
                Tmax_rcp85_2050.max().max()]) - 273.15
    # All data
    plt.figure()
    plt.subplot(211)
    plt.hist((Tmax_rcp45_2010-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmax_rcp45_2050-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.ylabel('Number')
    plt.legend(('2010s','2050s'),loc='best')
    plt.title(city[1].city + ', ' + city[1].state + '  Maximum Temperature')
    plt.text(Tmin,10,'RCP 4.5')
    plt.subplot(212)
    plt.hist((Tmax_rcp85_2010-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmax_rcp85_2050-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.xlabel('Temperature (C)')
    plt.ylabel('Number')
    plt.text(Tmin,10,'RCP 8.5')
    plt.show()
    #savefig(d + 'plots/' + city[1].city + '_tasmax.png')
    plt.close('all')
    
    # Winter
    Tmax_rcp45_2010['month'] = Tmax_rcp45_2010.index.month
    Tmax_rcp45_2050['month'] = Tmax_rcp45_2050.index.month
    wi2010 = np.logical_or(np.logical_or((Tmax_rcp45_2010.month==1),(Tmax_rcp45_2010.month==2)), (Tmax_rcp45_2010.month==12))
    wi2050 = np.logical_or(np.logical_or((Tmax_rcp45_2050.month==1),(Tmax_rcp45_2050.month==2)), (Tmax_rcp45_2050.month==12))
    sp2010 = np.logical_and((Tmax_rcp45_2010.month>=3),(Tmax_rcp45_2010.month<=5))
    sp2050 = np.logical_and((Tmax_rcp45_2050.month>=3),(Tmax_rcp45_2050.month<=5))
    su2010 = np.logical_and((Tmax_rcp45_2010.month>=6),(Tmax_rcp45_2010.month<=8))
    su2050 = np.logical_and((Tmax_rcp45_2050.month>=6),(Tmax_rcp45_2050.month<=8))
    fa2010 = np.logical_and((Tmax_rcp45_2010.month>=9),(Tmax_rcp45_2010.month<=11))
    fa2050 = np.logical_and((Tmax_rcp45_2050.month>=9),(Tmax_rcp45_2050.month<=11))
    Tmax_rcp45_2010 = Tmax_rcp45_2010.drop(columns='month')
    Tmax_rcp45_2050 = Tmax_rcp45_2050.drop(columns='month')

    plt.figure()
    plt.subplot(211)
    plt.hist((Tmax_rcp45_2010[wi2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmax_rcp45_2050[wi2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step',  color='red', alpha=0.3)
    plt.hist((Tmax_rcp45_2010[sp2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmax_rcp45_2050[sp2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step',  color='red', alpha=0.3)
    plt.hist((Tmax_rcp45_2010[su2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmax_rcp45_2050[su2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step',  color='red', alpha=0.3)
    plt.hist((Tmax_rcp45_2010[fa2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmax_rcp45_2050[fa2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step',  color='red', alpha=0.3)
    plt.ylabel('Number')
    plt.legend(('2010s','2050s'))
    plt.title(city[1].city + ', ' + city[1].state + '  Maximum Temperature')
    plt.text(Tmin,10,'RCP 4.5')
    plt.subplot(212)
    Tmax_rcp85_2010['month'] = Tmax_rcp85_2010.index.month
    Tmax_rcp85_2050['month'] = Tmax_rcp85_2050.index.month
    wi2010 = np.logical_or(np.logical_or((Tmax_rcp85_2010.month==1),(Tmax_rcp85_2010.month==2)), (Tmax_rcp85_2010.month==12))
    wi2050 = np.logical_or(np.logical_or((Tmax_rcp85_2050.month==1),(Tmax_rcp85_2050.month==2)), (Tmax_rcp85_2050.month==12))
    sp2010 = np.logical_and((Tmax_rcp85_2010.month>=3),(Tmax_rcp85_2010.month<=5))
    sp2050 = np.logical_and((Tmax_rcp85_2050.month>=3),(Tmax_rcp85_2050.month<=5))
    su2010 = np.logical_and((Tmax_rcp85_2010.month>=6),(Tmax_rcp85_2010.month<=8))
    su2050 = np.logical_and((Tmax_rcp85_2050.month>=6),(Tmax_rcp85_2050.month<=8))
    fa2010 = np.logical_and((Tmax_rcp85_2010.month>=9),(Tmax_rcp85_2010.month<=11))
    fa2050 = np.logical_and((Tmax_rcp85_2050.month>=9),(Tmax_rcp85_2050.month<=11))
    Tmax_rcp85_2010 = Tmax_rcp85_2010.drop(columns='month')
    Tmax_rcp85_2050 = Tmax_rcp85_2050.drop(columns='month')
    plt.hist((Tmax_rcp85_2010[wi2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmax_rcp85_2050[wi2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.hist((Tmax_rcp85_2010[sp2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmax_rcp85_2050[sp2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.hist((Tmax_rcp85_2010[su2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmax_rcp85_2050[su2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.hist((Tmax_rcp85_2010[fa2010]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmax_rcp85_2050[fa2050]-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.xlabel('Temperature (C)')
    plt.ylabel('Number')
    plt.text(Tmin,10,'RCP 8.5')
    plt.show()
    #savefig(d + 'plots/' + city[1].city + '_tasmax_winter.png')
    plt.close('all')



#%% Tmin
for city in cities.iterrows():
    Tmin_rcp45_2010 = pd.read_csv(d + city[1].city + '_tasmin_4.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmin_rcp45_2050 = pd.read_csv(d + city[1].city + '_tasmin_4.5_2044_2056.csv', index_col='time', parse_dates=True)
    Tmin_rcp85_2010 = pd.read_csv(d + city[1].city + '_tasmin_8.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmin_rcp85_2050 = pd.read_csv(d + city[1].city + '_tasmin_8.5_2044_2056.csv', index_col='time', parse_dates=True)
    
    Tmin = np.min([Tmin_rcp45_2010.min().min(),
                Tmin_rcp85_2010.min().min(),
                Tmin_rcp45_2050.min().min(),
                Tmin_rcp85_2050.min().min()]) - 273.15
    Tmax = np.min([Tmin_rcp45_2010.max().max(),
                Tmin_rcp85_2010.max().max(),
                Tmin_rcp45_2050.max().max(),
                Tmin_rcp85_2050.max().max()]) - 273.15
    
    plt.figure()
    plt.subplot(211)
    plt.hist((Tmin_rcp45_2010-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue', alpha=0.3)
    plt.hist((Tmin_rcp45_2050-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.ylabel('Number')
    plt.legend(('2010s','2050s'),loc='best')
    plt.title(city[1].city + ', ' + city[1].state + '  Minimum Temperature')
    plt.text(Tmin,10,'RCP 4.5')
    plt.subplot(212)
    plt.hist((Tmin_rcp85_2010-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='blue',alpha=0.3)
    plt.hist((Tmin_rcp85_2050-273.15).values.flatten(),bins=np.arange(Tmin,Tmax,1), histtype='step', color='red', alpha=0.3)
    plt.xlabel('Temperature (C)')
    plt.ylabel('Number')
    plt.text(Tmin,10,'RCP 8.5')
    plt.show()

    #savefig(d + 'plots/' + city[1].city + '_tasmin.png')
    

#%% Tmax - Tmin
for city in cities.iterrows():
    Tmax_rcp45_2010 = pd.read_csv(d + city[1].city + '_tasmax_4.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmax_rcp45_2050 = pd.read_csv(d + city[1].city + '_tasmax_4.5_2044_2056.csv', index_col='time', parse_dates=True)
    Tmax_rcp85_2010 = pd.read_csv(d + city[1].city + '_tasmax_8.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmax_rcp85_2050 = pd.read_csv(d + city[1].city + '_tasmax_8.5_2044_2056.csv', index_col='time', parse_dates=True)
    Tmin_rcp45_2010 = pd.read_csv(d + city[1].city + '_tasmin_4.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmin_rcp45_2050 = pd.read_csv(d + city[1].city + '_tasmin_4.5_2044_2056.csv', index_col='time', parse_dates=True)
    Tmin_rcp85_2010 = pd.read_csv(d + city[1].city + '_tasmin_8.5_2009_2020.csv', index_col='time', parse_dates=True)
    Tmin_rcp85_2050 = pd.read_csv(d + city[1].city + '_tasmin_8.5_2044_2056.csv', index_col='time', parse_dates=True)

    Td_rcp45_2010 = Tmax_rcp45_2010 - Tmin_rcp45_2010
    Td_rcp45_2050 = Tmax_rcp45_2050 - Tmin_rcp45_2050
    Td_rcp85_2010 = Tmax_rcp85_2010 - Tmin_rcp85_2010
    Td_rcp85_2050 = Tmax_rcp85_2050 - Tmin_rcp85_2050
    
    plt.figure()
    plt.subplot(211)
    plt.hist(Td_rcp45_2010.values.flatten(),bins=np.arange(0,30,1), histtype='step', color='blue', alpha=0.3)
    plt.hist(Td_rcp45_2050.values.flatten(),bins=np.arange(0,30,1), histtype='step', color='red', alpha=0.3)
    plt.ylabel('Number')
    plt.legend(('2010s','2050s'))
    plt.title(city[1].city + ', ' + city[1].state + '  Maximum minus Minimum Temperature')
    plt.text(1,10,'RCP 4.5')
    plt.subplot(212)
    plt.hist(Td_rcp85_2010.values.flatten(),bins=np.arange(0,30,1), histtype='step', color='blue',alpha=0.3)
    plt.hist(Td_rcp85_2050.values.flatten(),bins=np.arange(0,30,1), histtype='step', color='red', alpha=0.3)
    plt.xlabel('Temperature (C)')
    plt.ylabel('Number')
    plt.text(1,10,'RCP 8.5')
    #savefig(d + 'plots/' + city[1].city + '_tasmax-tasmin.png')
    plt.close('all')
