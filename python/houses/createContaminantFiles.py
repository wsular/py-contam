# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 12:29:52 2019

@author: Von P. Walden, Washington State University
"""
from glob import glob
import pandas as pd
import numpy  as np

def readWRF_CMAQfile(gridFile, dataFile, lat, lon, vrs, eqs, wthFlag):
    """
    This function reads data from a WRF CMAQ data file into pandas dataframes,
    ctm and wth. The dataframes can then be written to CONTAM contaminant and 
    weather files using functions, writeContamSpeciesFile and 
    writeContamWeatherFile.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                     2 Jun 2017
        Updated:    25 Feb 2019 - Simplified original code created by Kevin Toombs.
    """    
    # Open the WRF GRIDCRO2D file to determine the WRF pixel for lat/lon.
    GRID = xr.open_dataset(gridFile)
    ilat, ilon = find_WRF_pixel(GRID.LAT[0,0,:,:].values,GRID.LON[0,0,:,:].values,lat,lon)
    # Open WRF-CMAQ data file.
    print('Reading: ', dataFile)
    DATA = xr.open_dataset(dataFile)
    # Create a datetime index.
    datestr = str(DATA.SDATE)
    date    = datetime(int(datestr[0:4]),1,1) + timedelta(int(datestr[4:])-1)
    time    = [date + timedelta(hours=float(t)) for t in DATA.TSTEP]
    #
    # ............................... CONTAMINANT DATA ............................
    #
    # Create a pandas dataframe with contaminant variables.
    ctm = pd.DataFrame({},index=time)
    #ctm = ctm.set_index(pd.DatetimeIndex(ctm.index))
    
    for x in range(len(vrs)):
        vr = vrs.values[x]
        eq = eqs.values[x]
        dat = DATA[vr].values[:,0,ilat,ilon]
        
        #print(eq)
        if(eq[-1] == 'S'):
            air = DATA['AIR_DENS'].values[:,0,ilat,ilon]
            dat = dat/1000000000/air
            #dat.apply(lambda x: x/1000000000/AIR_DENS)
        else:
            pass
            split_eq = eq.split('/')
            mid_split = split_eq[1].split('*')
            base = float(mid_split[0])
            snd = float(mid_split[1])
            thrd = float(split_eq[2])
            dat = dat / base * snd / thrd
            
        
        ctm[vr] = dat

    # ........................... WEATHER DATA ............................
    #
    # Read contaminat data from WRF-CMAQ data file.
    if(wthFlag):
        if('AIR_DENS' in DATA):
            T    = DATA.SFC_TMP.values[:,0,ilat,ilon] + 273.15   # in K
            P    = DATA.AIR_DENS.values[:,0,ilat,ilon]*287.0*T
            wspd = DATA.WSPD10.values[:,0,ilat,ilon]
            wdir = DATA.WDIR10.values[:,0,ilat,ilon]
            # Conversion from relative humidity to mixing ration 
            #    ....http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
            A    = 6.116441
            m    = 7.591386
            Tn   = 240.7263
            es   = A*10**(m*(T-273.15)/(T-273.15+Tn))
            ws   = 0.622 * (es/P)
            w    = DATA.RH.values[:,0,ilat,ilon] * ws * 1000.  # Factor of 1000 converts from kg/kg to g/kg.
            
            # Create a pandas dataframe with meteorological variables.
            wth   = pd.DataFrame({'Ta':T, 
                                  'Pb':P,
                                  'Ws':wspd,
                                  'Wd':wdir,
                                  'Hr':w},
                                index=time)
    else:
        wth = pd.DataFrame({})
    
    GRID.close()
    DATA.close()
    return ctm, wth

def writeContamSpeciesFile(specFile, df):
    """
    This function writes the data in the pandas dataframe, df, to a text file.
    The text file is formatted as a CONTAM species file.

    """
    # Open new file.
    fp = open(specFile, 'w')
    
    # Write the first header lines.
    fp.write('SpeciesFile ContamW 2.0 ! file and version identification\n\n\n');
    fp.write(df.index[0].to_pydatetime().strftime('%m/%d')  + '\t');
    fp.write(df.index[-1].to_pydatetime().strftime('%m/%d') + '\t' + str(len(df.columns)) + '\n');
    fp.write('\t'.join(df.columns.values.tolist()) + '\n');
    # Write the hourly df.
    for hour in df.index:
        fp.write(  hour.strftime('%m/%d') + '\t'
                 + hour.strftime('%H:%M:%S') + '\t'
                 + '\t'.join([str(x) for x in df.loc[hour].values.tolist()]) +'\n')
    
    # Close the file.
    fp.close()
    
    return

# ######################## Main  
d = '/Users/vonw/data/iaq/houses/outdoors/'
directories = glob(d + '*.xlsx')
directories.sort()

for directory in directories:
    rack  = pd.read_csv(directory.split('.')[0] + '/' + 'outdoor_rack-Table 1.csv',
                        na_filter=True,
                        header=[0,1],
                        parse_dates=[0],
                        sep="\s*,\s*")     # sep is necessary to remove whitespace.
    pm25  = pd.read_csv(directory.split('.')[0] + '/' + 'PM2.5-Table 1.csv',
                        na_filter=True,
                        header=[0,1],
                        parse_dates=[0],
                        sep="\s*,\s*")     # sep is necessary to remove whitespace.
    ptrms = pd.read_csv(directory.split('.')[0] + '/' + 'PTR-MS-Table 1.csv',
                        na_filter=True,
                        header=[0,1],
                        parse_dates=[0])
                        sep="\s*,\s*")     # sep is necessary to remove whitespace.
        