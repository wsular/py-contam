# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:41:45 2017

@author: Von P. Walden, Washington State University
"""

import xarray as xr
import numpy  as np
import pandas as pd
from   datetime import datetime, timedelta

def find_WRF_pixel(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    # Renamed findWRFpixel from original function, naive_fast, written by Vikram Ravi.
    latvals = latvar[:]
    lonvals = lonvar[:]
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)


directory = '/Users/vonw/data/iaq/cmaq/'

lat = 46.7
lon = -117.2

# Open the WRF GRIDCRO2D file to determine the WRF pixel for lat/lon.
GRID = xr.open_dataset(directory + 'GRIDCRO2D_19941215')
ilat, ilon = find_WRF_pixel(GRID.LAT[0,0,:,:].values,GRID.LON[0,0,:,:].values,lat,lon)

# Open WRF-CMAQ data file.
DATA = xr.open_dataset(directory + 'extr/rcp8.5/2040ei_v6_cb05v2_ref_RCP8.5.combine.aconc.2050.01')
# Create a datetime index.
datestr = str(DATA.SDATE)
date    = datetime(int(datestr[0:4]),1,1) + timedelta(int(datestr[4:])-1)
time    = [date + timedelta(hours=float(t)) for t in DATA.TSTEP]
# ...
# Read meteological data from WRF-CMAQ data file.
T    = DATA.SFC_TMP.values[:,0,ilat,ilon] + 273.15   # in K
P    = DATA.AIR_DENS.values[:,0,ilat,ilon]*287.0*T
wspd = DATA.WSPD10.values[:,0,ilat,ilon]
wdir = DATA.WDIR10.values[:,0,ilat,ilon]
# Conversion from relative humidity to mixing ration 
#    ....http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
A    = 6.116441
m    = 7.591386
Tn   = 240.7263
es   = A*10**(A*(T-273.15)/(T-273.15+Tn))
ws   = 0.622 * (es/P)
w    = DATA.RH.values[:,0,ilat,ilon] * ws * 1000.  # Factor of 1000 converts from kg/kg to g/kg.

# Create a pandas dataframe with meteorological variables.
df   = pd.DataFrame({'Ta':T, 
                     'Pb':P,
                     'Ws':wspd,
                     'Wd':wdir,
                     'Hr':w},
                     index=time)

