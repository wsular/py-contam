# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 14:22:16 2017

@author: WSU-LAR-NATHAN
"""

import matplotlib.pyplot as plt
import numpy as np
import os
from netCDF4 import Dataset
#%%
#Clear working space
clear = lambda: os.system('cls')
clear()
inputDir = "D:\WSU-LAR-NATHAN\Documents\Lab\cmaq"
#Set working directory
#os.chdir('D:\WSU-LAR-NATHAN\Documents\Lab\cmaq\out\rcp4.5')#DIRECTORY WILL CHANGE

#%%
def naive_fast(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    latvals = latvar[:]
    lonvals = lonvar[:]
    ny,nx = latvals.shape
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

#%%
# get the grid information
gridcroFile = metdir + begin_date.strftime('%Y%m%d') +'00' + '/MCIP/GRIDCRO2D'
grd = Dataset(gridcroFile,'r')
lat = grd.variables['LAT'][0,0,:,:]
lon = grd.variables['LON'][0,0,:,:]
grd.close()
 
#%%
iy,ix = naive_fast(lat, lon, 48.20, -120.80)
pgts_file = inputDir + "/" + "2040ei_v6_cb05v2_ref_RCP4.5.combine.aconc.2050.01"
concFile = Dataset(pgts_file, 'r')
pmfine = concFile.variables['PMFINE'][:,:,:,:]
concFile.close()
#%%
fig, ax = plt.subplots()
y=[]
x=[]   
for t in np.arange(0,24):
    x.append(t)
    y.append(0)
    conc = pmfine[t,:,iy,ix]
