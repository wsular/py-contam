# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:45:00 2018

@author: Von P. Walden, Washington State University
"""
#%%
import contam_output
import os
import subprocess
from shutil import copy2
import cupy  as cp
import cudf
from glob import glob
import pandas as pd
import xarray as xr

#%%
################################## USER INPUT ###############################
# Select a directory for your CONTAM simulations
output = 'VonTest'

# Indoor air temperature in F; 66, 70, or 74
indoorAirTemp    = 70

# Representative Concentration Pathway (RCP); 4.5 or 8.5
#    Must be a floating-point number
rcps = (4.5, 8.5)

# U.S. cities from the following list:
#    'Atlanta', 'Boston', 'Burmingham', 'Buffalo', 'Chicago', 'Cincinatti', 
#    'CorpusChristi', 'Dallas', 'Denver', 'LosAngeles', 'Miami', 'Minneapolis', 
#    'Nashville', 'NewYork', 'Phoenix', 'Seattle', 'St.Louis', 'Washington', 'Worcester'
#
#    Note: if only one city is chosen, then make it a list (['Chicago']), not a string.
#
cities = ('Atlanta', 'Boston', 'Birmingham', 'Buffalo', 'Chicago', 'Cincinnati', 'CorpusChristi', 'Dallas', 'Denver', 'LosAngeles', 'Miami', 'Minneapolis', 'Nashville', 'NewYork', 'Phoenix', 'Seattle', 'St.Louis', 'Washington', 'Worcester')

# House type; 'AH-1', DH-1', 'DH-3', 'House-5', 'MH-1'
#
#    Note: if only one house is chosen, then make it a list (['DH-1']), not a string.
#
houses = ('AH-1', 'DH-1', 'DH-3', 'House-5', 'MH-1')
nodes  = ('Cnd8', 'Cnd8', 'Cnd5', 'Cnd6', 'Cnd5')         # Contaminant node in each house to examine; these get zipped together.

# Simulation years from the following list:
#    (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
#     2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055,
#     2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098)
years = (2086, 2087)

# CMIP5 climate change models from the following list:
#    'CCSM4', 'CNRM-CM5', 'GFDL-ESM2M', 'HadGEM2-ES365', 
#     'IPSL-CM5A-LR', 'MIROC5', 'MIROC-ESM'
#
#    Note: if only one model is chosen, then make it a list (['CCSM4']), not a string.
#
models = ('CCSM4', 'CNRM-CM5', 'GFDL-ESM2M', 'HadGEM2-ES365', 'IPSL-CM5A-LR', 'MIROC5', 'MIROC-ESM')
#############################################################################

#%%
# Create new directory or quit if it already exists! No way to write over data.
outdir = '/mnt/data/lima/iaq/cmaq/prjFiles/' + output + '/'
if not os.path.exists(outdir):
    os.makedirs(outdir)
else:
    print('The desired output directory ALREADY EXISTS! Try again...')
    quit()

# Copy this file, runContam.py,	to the output directory	for documentation.
copy2('/mnt/data/lima/iaq/cmaq/runContam.py', outdir);

# Sets directories that contain weather and contaminant files.
wthdir = '/mnt/data/lima/iaq/contam_modeling/modeling_future_climate/weatherFiles/'
ctmdir = '/mnt/data/lima/iaq/contam_modeling/modeling_future_climate/contaminantFiles/'

#houses    = glob('/mnt/data/lima/iaq/home_models/' + str(indoorAirTemp) + 'findoortemp/*.prj')
site_data = pd.read_csv('/mnt/data/lima/iaq/cmaq/sites.csv')

#%%
############################ CREATE PRJ FILES ###############################
def createContamPrjFile(outdir, city, year, rcp, model, house, indoorAirTemp):
    ### 
    # Function to create a contam project (prj) file based on desired input. 
    # 
    # Created by Von P. Walden, Washington State University
    #            15 Dec 2018
    ###
    # Read in contam project file template.
    houseFile = '/mnt/data/lima/iaq/contam_modeling/modeling_future_climate/' + str(indoorAirTemp) + 'findoortemp/' + house + '.prj'
    lines   = open(houseFile, 'r').readlines()
    prjFile = list(lines)
    # Determine paths to weather and contaminant files
    wthpath = wthdir + city.iloc[0].City_Name + '_' + year + '_' + rcp + '_' + model + '.wth'
    ctmpath = ctmdir + year + '_rcp' + rcp + '_' + city.iloc[0]['City_Name'] + '.ctm'
    # Replace lines in template with desired information.
    prjFile[9]  = wthpath + ' ! weather file\n'
    prjFile[10] = ctmpath + ' ! contaminant file\n'
    prjFile[21] = ' {:>6} {:>6} {:>6} {:>6} 283.15 2 0\n'.format(city.iloc[0].Latitude, city.iloc[0].Longitude,city.iloc[0].tznr,city.iloc[0].altd)
    prjFile[38] = ('  Jan01 00:00:00  Jan01 00:00:00  Dec31 23:00:00  01:00:00 01:00:00 01:00:00\n')
    # Write new contam project file
    with open(outdir+house+'.prj'+ctmpath.split('/')[-1]+wthpath.split('/')[-1]+'.prj','w') as out: out.writelines(prjFile)
    return

for city in cities:
    city_data = site_data.loc[site_data['City_Name']==city]
    for year in years:
        for rcp in rcps:
            for model in models:
                for house in houses:
                    createContamPrjFile(outdir, city_data, str(year), str(rcp), model, house, indoorAirTemp)
#############################################################################

#%%
############################# RUN PRJ FILES #################################
os.chdir(outdir)
prjFiles = glob(outdir+'*.prj')
prjFiles.sort()
for prjFile in prjFiles:
    print(prjFile)
    # Run contam, but suppress all the output.
    #    https://stackoverflow.com/questions/4760215/running-shell-command-and-capturing-the-output
    result = subprocess.run(['/mnt/data/lima/contam/contam-x-3.2-gcc.exe',prjFile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#############################################################################

#%%
########################### CREATE netCDF SUMMARY FILE ########################
def readAmbient(house, year, rcp, city):
    # Initialize dataframes.
    T     = cudf.DataFrame({})
    ws    = cudf.DataFrame({})
    oCtm1 = cudf.DataFrame({})
    oCtm2 = cudf.DataFrame({})
    oCtm3 = cudf.DataFrame({})
    # Loop over models.
    for model in models:
        fn  = house + '.prj' + str(year) + '_rcp' + str(rcp) + '_' + city + '.ctm' + city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth.sim'
        #print(d + fn)   # for testing
        sim          = contam_output.Contam(outdir + fn)
        amb          = sim.readAmbient()
        amb.index    = amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
        T[model]     = amb.Tambt
        ws[model]    = amb.Ws
        oCtm1[model] = amb.Ctm1
        oCtm2[model] = amb.Ctm2
        oCtm3[model] = amb.Ctm3
        
    return T, ws, oCtm1, oCtm2, oCtm3
                        
def readContaminants(house, year, rcp, city, node):
    # Initialize dataframes.
    ctm1 = cudf.DataFrame({})
    ctm2 = cudf.DataFrame({})
    ctm3 = cudf.DataFrame({})
    # Loop over models.
    for model in models:
        fn  = house + '.prj' + str(year) + '_rcp' + str(rcp) + '_' + city + '.ctm' + city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth.sim'
        sim       = contam_output.Contam(outdir + fn)
        ctm       = sim.readContaminantNodes()
        ctm['ctm1'].index = ctm['ctm1'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
        ctm['ctm2'].index = ctm['ctm2'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
        ctm['ctm3'].index = ctm['ctm3'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
        ctm1[model]  = ctm['ctm1'][node]
        ctm2[model]  = ctm['ctm2'][node]
        ctm3[model]  = ctm['ctm3'][node]
                        
    return ctm1, ctm2, ctm3

def readACH(house, year, rcp, city):
    # Initialize dataframes.
    ach = cudf.DataFrame({})
    # Loop over models.
    for model in models:
        fn    = house + '.prj' + str(year) + '_rcp' + str(rcp) + '_' + city + '.ctm' + city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth.ach'
        achp  = pd.read_csv(outdir + fn, sep='\t', skiprows=1)
        dates = [pd.datetime(year,int(m),int(d)) for m,d in [date.split('/') for date in achp.day]]
        hours = [int(hr[0:2]) for hr in achp.time]
        achp.index = [date + pd.to_timedelta(hour, 'h') for date, hour in zip(dates,hours)]
        ach[model]  = achp.total

    return ach

first = True
for rcp in rcps:
    for house, node in zip(houses, nodes):
        for city in cities:
            print('Processing: ', rcp, house, city)
            # Ambient meteorology and outside contaminants
            T     = cudf.DataFrame({})
            W     = cudf.DataFrame({})
            octm1 = cudf.DataFrame({})
            octm2 = cudf.DataFrame({})
            octm3 = cudf.DataFrame({})
            # Contaminants
            ctm1 = cudf.DataFrame({})
            ctm2 = cudf.DataFrame({})
            ctm3 = cudf.DataFrame({})
            # ACH
            ach  = cudf.DataFrame({})
            for year in years:
                # Ambient
                Tp, Wp, O1p, O2p, O3p = readAmbient(house, year, rcp, city)
                T      = cudf.concat([T, Tp])
                W      = cudf.concat([W, Wp])
                octm1  = cudf.concat([octm1, O1p])
                octm2  = cudf.concat([octm2, O2p])
                octm3  = cudf.concat([octm3, O3p])
                # Contaminants
                c1, c2, c3 = readContaminants(house, year, rcp, city, node)
                ctm1 = cudf.concat([ctm1, c1])
                ctm2 = cudf.concat([ctm2, c2])
                ctm3 = cudf.concat([ctm3, c3])
                # ACH
                a    = readACH(house, year, rcp, city)
                ach  = cudf.concat([ach, a])
            # Unit conversions
            T = T-273.15  # convert to C
            octm1 = octm1 * 1e9 * (28.97/30.03)   # Convert to ppb
            octm2 = octm2 * 1e9 * (28.97/48.)     # Convert to ppb
            octm3 = octm3 * 1e9 * 1.25            # Convert to ug m-3
            ctm1 = ctm1 * 1e9 * (28.97/30.03)     # Convert to ppb
            ctm2 = ctm2 * 1e9 * (28.97/48.)       # Convert to ppb
            ctm3 = ctm3 * 1e9 * 1.25              # Convert to ug m-3
            # Save data file.
            if first:
                times    = T.to_pandas().index
                da_T     = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': '2-meter outside air temperature', 'units': 'deg C'})
                da_W     = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': '10-meter outside wind speed', 'units': 'm s-1'})
                da_octm1 = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Outside concentration of formaldehyde (HCHO)', 'units': 'ppb'})
                da_octm2 = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Outside concentration of ozone (O3)', 'units': 'ppb'})
                da_octm3 = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Outside concentration of particulate matter less than 2.5 microns (PM2.5)', 'units': 'micrograms m-3'})
                da_ctm1  = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Inside concentration of formaldehyde (HCHO)', 'units': 'ppb'})
                da_ctm2  = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Inside concentration of ozone (O3)', 'units': 'ppb'})
                da_ctm3  = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Inside concentration of particulate matter less than 2.5 microns (PM2.5)', 'units': 'micrograms m-3'})
                da_ach   = xr.DataArray(cp.asnumpy(cp.ones((len(rcps),len(models),len(cities),len(houses),len(times)))*cp.nan), dims=['rcp', 'model', 'city', 'house', 'time'], coords=[list(rcps), list(models), list(cities), list(houses), times], attrs={'long_name': 'Air changes per hour', 'units': 'air changes hr-1'})
                first = False
            for model in models:
                da_T.loc[rcp, model, city, house]     = T[model].to_pandas().values
                da_W.loc[rcp, model, city, house]     = W[model].to_pandas().values
                da_octm1.loc[rcp, model, city, house] = octm1[model].to_pandas().values
                da_octm2.loc[rcp, model, city, house] = octm2[model].to_pandas().values
                da_octm3.loc[rcp, model, city, house] = octm3[model].to_pandas().values
                da_ctm1.loc[rcp, model, city, house]  = octm1[model].to_pandas().values
                da_ctm2.loc[rcp, model, city, house]  = ctm2[model].to_pandas().values
                da_ctm3.loc[rcp, model, city, house]  = ctm3[model].to_pandas().values
                da_ach.loc[rcp, model, city, house]   = ach[model].to_pandas().values

contam = xr.Dataset({'T': da_T, 
                     'W': da_W,
                     'octm1': da_octm1,
                     'octm2': da_octm2,
                     'octm3': da_octm3,
                     'ctm1': da_ctm1,
                     'ctm2': da_ctm2,
                     'ctm3': da_ctm3,
                     'ach': da_ach,
                     'indoorAirTemperature': (indoorAirTemp-32)*(5/9)
                    })
contam.indoorAirTemperature['long_name'] = 'Inside air temperature'
contam.indoorAirTemperature['units'] = 'deg C'

contam.to_netcdf(outdir+output+'.nc')
#############################################################################

# %%
