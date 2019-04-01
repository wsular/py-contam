#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 13:21:58 2019

@author: Von P. Walden, Laboratory for Atmospheric Research, Washington State University
"""

import xarray as xr
import pandas as pd
import numpy as np
from   datetime import datetime, timedelta


##############################################################################
def find_WRF_pixel(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    # Renamed findWRFpixel from original function, naive_fast, written by Vikram Ravi.
    latvals = latvar[:]
    lonvals = lonvar[:]
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

def read_datafile(gridFile, dataFile, lat, lon, vrs, eqs, wthFlag):
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

##############################################################################
# Main program
extr_dir1   = '/Volumes/vonw/cmaq/DOE_20years/36km/'
output_dir  = '/Users/vonw/data/iaq/cmaq/output/'

variables   = pd.read_csv('/Users/vonw/work/software/iaq/py-contam/python/vrs.csv')
sites       = pd.read_csv('/Users/vonw/work/software/iaq/py-contam/python/iaq_cities.csv')

years  = [2095]
months = range(1,13)
rcps   = ['RCP4.5', 'RCP8.5']
for row, site in sites.iterrows():
#    if(site.city != 'Chicago'): break    # !! For testing only !!
    for rcp in rcps:
        extr_dir2   = '/Volumes/sdata/cmaq/cmaq5.2/' + rcp.lower() + '/extr/'
        for year in years:
            # Initialize DataFrames
            ctm    = pd.DataFrame({})
            wth    = pd.DataFrame({})
            for month in months:
                if ( (year>=1996) & (year<=2005)):
                    gridFile   = '/Volumes/sdata/cmaq/GRIDCRO2D_2086-2095'
                    dataFile = extr_dir1 + str(year) + '/CCTM_DOE_36km_SF_RERUN_combine.aconc.' + str(year) + str(month).zfill(2)
                elif( (year>=2046) & (year<=2055)):
                    gridFile   = '/Volumes/sdata/cmaq/GRIDCRO2D_2046-2055'
                    dataFile = extr_dir2 + '2040ei_v6_cb05v2_ref_' + rcp + '.combine.aconc.' + str(year) + '.' + str(month).zfill(2)
                elif( (year>=2086) & (year<=2095)):
                    gridFile   = '/Volumes/sdata/cmaq/GRIDCRO2D_2086-2095'
                    dataFile = extr_dir2 + '2040ei_v6_cb05v2_ref_' + rcp + '.combine.aconc.' + str(year) + '.' + str(month).zfill(2)
                
                # Read data from the WRF-CMAQ file.
                data = read_datafile(gridFile, 
                                     dataFile, 
                                     site.latitude, 
                                     site.longitude, 
                                     variables['Name'], 
                                     variables['Convert units'],
                                     False)
                ctm  = ctm.append(data[0])
                wth  = wth.append(data[1])
            
            # Create ctm file.
            writeContamSpeciesFile(output_dir + str(year) + '_' + rcp.lower() + '_' + site.city + '.ctm', ctm)
