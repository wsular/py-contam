#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 17:41:34 2019

@author:    Von P. Walden
            Washington State University
"""

import contam_output

d = '/mnt/data/lima/iaq/houses/outdoors/'
houses = ['h002_outdoor_summer',
          'h002_outdoor_winter',
          'h003_outdoor_summer',
          'h003_outdoor_winter',
          'h004_outdoor_summer',
          'h004_outdoor_winter',
          'h005_outdoor_summer',
          'h006_outdoor_summer',
          'h006_outdoor_winter',
          'h007_outdoor_summer',
          'h007_outdoor_winter',
          'h008_outdoor_summer',
          'h008_outdoor_winter',
          'h009_outdoor_summer',
          'h009_outdoor_winter',
          'h010_outdoor_summer']
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
          2017]

fn     = houses[6]
year   = years[6]
outdir = '/Users/vonw/data/iaq/houses/outdoors/'
house  = fn[-19:-15]
node   = 'Cnd1'

sim       = contam_output.Contam(outdir + fn + '/' + house + '.sim')
amb       = sim.readAmbient()
amb.index = amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
T  = amb.Tambt
ws = amb.Ws
oCtm1 = amb.Ctm1
oCtm2 = amb.Ctm2
oCtm3 = amb.Ctm3

ctm       = sim.readContaminantNodes()
ctm['ctm1'].index = ctm['ctm1'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
ctm['ctm2'].index = ctm['ctm2'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
ctm['ctm3'].index = ctm['ctm3'].index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
ctm1  = ctm['ctm1'][node]
ctm2  = ctm['ctm2'][node]
ctm3  = ctm['ctm3'][node]
                        


fns = [d + house + '/' + house for house in houses]
for fn in fns:
    house  = fn[-19:-15]
    season = fn[-6:]

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
    hdf = pd.HDFStore(outdir+output+'_rcp'+str(rcp)+'_'+indoorAirTemp+'F.hdf')
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

