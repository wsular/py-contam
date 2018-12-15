# -*- coding: utf-8 -*-
"""
Created on Fri Dec 15 13:45:00 2018

@author: Von P. Walden, Washington State University
"""
import contam_output
import os
import subprocess
import numpy  as np
import pandas as pd
from glob import glob

################################## USER INPUT ###############################

# Select a directory for your CONTAM simulations
output = 'testRun1'

# Indoor air temperature in F; '66', '70', or '74'
#    Must be a string
indoorAirTemp    = '70'   

# Representative Concentration Pathway (RCP); 4.5 or 8.5
#    Must be an integer
rcps   = (4.5, 8.5)

# U.S. cities from the following list:
#    'Atlanta', 'Boston', 'Burmingham', 'Buffalo', 'Chicago', 'Cincinatti', 
#    'CorpusChristi', 'Dallas', 'Denver', 'LosAngeles', 'Miami', 'Minneapolis', 
#    'Nashville', 'NewYork', 'Phoenix', 'Seattle', 'St.Louis', 'Washington', 'Worcester'
#
#    Note: if only one city is chosen, then make it a list (['Chicago']), not a string.
#
cities = ('Dallas', 'Denver', 'Phoenix', 'Washington')

# House type; 'AH-1', DH-1', 'DH-3', 'House-5', 'MH-1'
#
#    Note: if only one house is chosen, then make it a list (['DH-1']), not a string.
#
houses = ('DH-1', 'DH-3', 'House-5')
nodes  = ('Cnd8', 'Cnd5', 'Cnd6')         # Contaminant node in each house to examine; these get zipped together.

# Simulation years from the following list:
#    (2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
#     2047, 2048, 2049, 2050, 2051, 2052, 2053, 2054, 2055,
#     2090, 2091, 2092, 2093, 2094, 2095, 2096, 2097, 2098)
years = (2010, 2011, 2012)

# CMIP5 climate change models from the following list:
#    'CCSM4', 'CNRM-CM5', 'GFDL-ESM2M', 'HadGEM2-ES365', 
#     'IPSL-CM5A-LR', 'MIROC5', 'MIROC-ESM'
#
#    Note: if only one model is chosen, then make it a list (['CCSM4']), not a string.
#
models = ('CCSM4', 'CNRM-CM5', 'GFDL-ESM2M', 'HadGEM2-ES365', 'IPSL-CM5A-LR', 'MIROC5', 'MIROC-ESM')
#############################################################################

# Create new directory or quit if it already exists! No way to write over data.
outdir = '/mnt/data/lima/iaq/cmaq/prjFiles/' + output + '/'
if not os.path.exists(outdir):
    os.makedirs(outdir)
else:
    print('The desired output directory ALREADY EXISTS! Try again...')
    quit()

# Sets directories that contain weather and contaminant files.
wthdir = '/mnt/data/lima/iaq/contam/weatherFiles/'
ctmdir = '/mnt/data/lima/iaq/contam/contaminantFiles/'

#houses    = glob('/mnt/data/lima/iaq/home_models/' + str(indoorAirTemp) + 'findoortemp/*.prj')
site_data = pd.read_csv('/mnt/data/lima/iaq/cmaq/sites.csv')

############################ CREATE PRJ FILES ###############################
def createContamPrjFile(outdir, city, year, rcp, model, house, indoorAirTemp):
    ### 
    # Function to create a contam project (prj) file based on desired input. 
    # 
    # Created by Von P. Walden, Washington State University
    #            15 Dec 2018
    ###
    # Read in contam project file template.
    houseFile = '/mnt/data/lima/iaq/home_models/' + str(indoorAirTemp) + 'findoortemp/' + house + '.prj'
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

############################ CREATE HDF SUMMARY FILE ########################
def readAmbient(house, year, rcp, city):
    # Initialize dataframes.
    T    = pd.DataFrame({})
    ws   = pd.DataFrame({})
    oCtm1 = pd.DataFrame({})
    oCtm2 = pd.DataFrame({})
    oCtm3 = pd.DataFrame({})
    # Loop over models.
    for model in models:
        fn  = house + '.prj' + str(year) + '_rcp' + str(rcp) + '_' + city + '.ctm' + city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth.sim'
        #print(d + fn)   # for testing
        sim       = contam_output.Contam(outdir + fn)
        amb       = sim.readAmbient()
        amb.index = amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
        T[model]  = amb.Tambt
        ws[model] = amb.Ws
        oCtm1[model] = amb.Ctm1
        oCtm2[model] = amb.Ctm2
        oCtm3[model] = amb.Ctm3
        
    return T, ws, oCtm1, oCtm2, oCtm3
                        
def readContaminants(house, year, rcp, city, node):
    # Initialize dataframes.
    ctm1 = pd.DataFrame({})
    ctm2 = pd.DataFrame({})
    ctm3 = pd.DataFrame({})
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
    ach = pd.DataFrame({})
    # Loop over models.
    for model in models:
        fn    = house + '.prj' + str(year) + '_rcp' + str(rcp) + '_' + city + '.ctm' + city + '_' + str(year) + '_' + str(rcp) + '_' + model + '.wth.ach'
        achp  = pd.read_csv(outdir + fn, sep='\t', skiprows=1)
        dates = [pd.datetime(year,int(m),int(d)) for m,d in [date.split('/') for date in achp.day]]
        hours = [int(hr[0:2]) for hr in achp.time]
        achp.index = [date + pd.to_timedelta(hour, 'h') for date, hour in zip(dates,hours)]
        ach[model]  = achp.total

    return ach

for rcp in rcps:
    hdf = pd.HDFStore(outdir+'HouseSummaryData_rcp'+str(rcp)+'_'+indoorAirTemp+'F.hdf')
    for house, node in zip(houses, nodes):
        for city in cities:
            print('Processing: ', rcp, house, city)
            # Ambient meteorology and outside contaminants
            T     = pd.DataFrame({})
            W     = pd.DataFrame({})
            octm1 = pd.DataFrame({})
            octm2 = pd.DataFrame({})
            octm3 = pd.DataFrame({})
            # Contaminants
            ctm1 = pd.DataFrame({})
            ctm2 = pd.DataFrame({})
            ctm3 = pd.DataFrame({})
            # ACH
            ach  = pd.DataFrame({})
            for year in years:
                # Ambient
                Tp, Wp, O1p, O2p, O3p = readAmbient(house, year, rcp, city)
                T      = pd.concat([T, Tp])
                W      = pd.concat([W, Wp])
                octm1  = pd.concat([octm1, O1p])
                octm2  = pd.concat([octm2, O2p])
                octm3  = pd.concat([octm3, O3p])
                # Contaminants
                c1, c2, c3 = readContaminants(house, year, rcp, city, node)
                ctm1 = pd.concat([ctm1, c1])
                ctm2 = pd.concat([ctm2, c2])
                ctm3 = pd.concat([ctm3, c3])
                # ACH
                a    = readACH(house, year, rcp, city)
                ach  = pd.concat([ach, a])
            # Unit conversions
            T = T-273.15  # convert to C
            octm1 = octm1 * 1e9 * (28.97/30.03)   # Convert to ppb
            octm2 = octm2 * 1e9 * (28.97/48.)     # Convert to ppb
            octm3 = octm3 * 1e9 * 1.25            # Convert to ug m-3
            ctm1 = ctm1 * 1e9 * (28.97/30.03)     # Convert to ppb
            ctm2 = ctm2 * 1e9 * (28.97/48.)       # Convert to ppb
            ctm3 = ctm3 * 1e9 * 1.25              # Convert to ug m-3
            # Save data file.
            hdf.put(house+'/'+city+'/T', T)
            hdf.put(house+'/'+city+'/W', W)
            hdf.put(house+'/'+city+'/octm1', octm1)
            hdf.put(house+'/'+city+'/octm2', octm2)
            hdf.put(house+'/'+city+'/octm3', octm3)
            hdf.put(house+'/'+city+'/ctm1', ctm1)
            hdf.put(house+'/'+city+'/ctm2', ctm2)
            hdf.put(house+'/'+city+'/ctm3', ctm3)
            hdf.put(house+'/'+city+'/ach', ach)

    hdf.close()
#############################################################################
