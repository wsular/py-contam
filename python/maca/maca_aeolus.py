# -*- coding: utf-8 -*-
"""
Created on Mon Feb  8 15:12:49 2016

@author: Von P. Walden, Washington State University

Python module for extracting data from the MACA version 2 downscaled data that were generated using
the METDATA product for historical data. Users should consult and cite the following publications
related to these data:

    Abatzoglou, J. T., & Brown, T. J. (2011). A comparison of statistical downscaling methods suited 
    for wildfire applications. Int J Climatol, 32(5), 772-780. doi:10.1002/joc.2312 

    Abatzoglou, J. T. (2013). Development of gridded surface meteorological data for ecological 
    applications and modelling. Int J Climatol, 33(1), 121-131. 

Input Parameters:
    Users must specify the following variables to use this function:
        fvar - file variable (Only a single variable can be accessed at a time.)
                pr      = precipitation
                rsds    = downwelling solar radiation
                tasmax  = maximum temperature
                tasmin  = minimum temperature
                uas     = eastward wind
                vas     = northward wind
                huss    = specific humidity
                rhmax   = maximum relative humidity
                rhmin   = minimum relative humidity

        models - CMIP5 model(s) to extract data for (This MUST be a Python list.)
                bcc-csm1-1
                BNU-ESM
                CanESM2
                CCSM4
                CNRM-CM5
                CSIRO-Mk3-6-0
                GFDL-ESM2G
                GFDL-ESM2M
                HadGEM2-CC365
                HadGEM2-ES365
                inmcm4
                IPSL-CM5A-LR
                IPSL-CM5A-MR
                IPSL-CM5B-LR
                MIROC-ESM
                MIROC-ESM-CHEM
                MIROC5
                MRI-CGCM3
                NorESM1-M

        rcp - Representative Concentration Pathway
                4.5
                8.5

        beginningDate - beginning data of extracted data (as a string)
                yyyy-mm-dd

        endingDate - beginning data of extracted data (as a string)
                yyyy-mm-dd

        latitude - latitude of extracted data
                decimal degrees North between -90. and 90.

        longitude - longitude of extracted data
                decimal degrees East between 0. and 360.

Output:
    A pandas DataFrame is returned that contains the output; the dates are used as the DataFrame index.

Example Usage:

# Example 1: Precipitation from a single CMIP5 model (NorESM1-M).
# Start ipython by typing /home/vonw/anaconda3/bin/ipython3 (or eqiuvalent)
%pylab
from maca_aeolus import maca
prcp = maca('pr',['NorESM1-M'],4.5,'1950-01-01','2006-12-31',46.7,360.-117.2)   # For Pullman, WA
prcp.plot()

# Example 2: Maximum daily temperature from a few CMIP5 models. (This may take a few minutes!!)
Tmax = maca('tasmax',['bcc-csm1-1', 'GFDL-ESM2M', 'NorESM1-M'],4.5,'1950-01-01','2006-12-31',46.7,360.-117.2)
Tmax.plot()

"""
def maca(fvar,models,rcp,beginningDate,endingDate,latitude,longitude):
    import numpy    as np
    import pandas   as pd
    import xarray   as xr
    from   netCDF4  import Dataset

    def getMACApixel(maca,lat,lon):    
        dlat = float(maca.geospatial_lat_resolution)/2.
        dlon = float(maca.geospatial_lon_resolution)/2.
        ilat = np.where((maca.variables['lat'][:] > lat-dlat) & (maca.variables['lat'][:] <= lat+dlat))[0][0]
        ilon = np.where((maca.variables['lon'][:] > lon-dlon) & (maca.variables['lon'][:] <= lon+dlon))[0][0]
        return ilat, ilon

    # INPUT PARAMETERS
    #fvar   = 'tasmax'
    #var    = 'air_temperature'
    #models = ['BNU-ESM']
    #rcp    = 4.5            # either 4.5. or 8.5
    bdate  = pd.to_datetime(beginningDate)
    edate  = pd.to_datetime(endingDate)
    #lat1   = 46.7
    #lon1   = 360-117.2

    # Data directory
    directory = '/Volumes/maca/'     # aeolus
    
    # Set variable name (var) based on the file variable (fvar).
    if ((fvar=='tasmax') | (fvar=='tasmin')):
    	var = 'air_temperature'
    elif ((fvar=='rhsmax') | (fvar=='rhsmin')):
    	var = 'relative_humidity'
    elif (fvar=='pr'):
    	var = 'precipitation'
    elif (fvar=='rsds'):
    	var = 'surface_downwelling_shortwave_flux_in_air'
    elif (fvar=='huss'):
    	var = 'specific_humidity'
    elif (fvar=='uas'):
    	var = 'eastward_wind'
    elif (fvar=='vas'):
    	var = 'northward_wind'
    else:
    	print('Error in specifying the file variable: Try again...')
    	return
    # Opens any MACA file simply to grab the lats and lons.
    maca   = Dataset(directory + 'macav2metdata_tasmax_BNU-ESM_r1i1p1_historical_1950_1954_CONUS_daily.nc')
    ilat, ilon = getMACApixel(maca,latitude,longitude)
    maca.close()

    # Transfrom rcp from number to str.
    if (rcp==4.5):
        rcp = '45'
    elif (rcp==8.5):
        rcp = '85'
    else:
        print('ERROR: Incorrect RCP!')

    # Sets up the information for the filenames.
    data      = pd.DataFrame(columns={'time', 'filename', 'byear', 'eyear'})
    for model in models:
        data[model] = None
    data.time=pd.date_range(bdate,edate)
    byear      = np.append(np.linspace(1950,2005,12), np.linspace(2006,2096,19))
    eyear      = np.append(np.append(np.append(np.linspace(1954,2004,11), 2005.), np.linspace(2010,2095,18)), 2099.)
    year_range = [[str(int(yr[0])), str(int(yr[1]))] for yr in zip(byear,eyear)]
    for yr in year_range:
        data.loc[(data.time>=pd.to_datetime(yr[0]+'-1-1')) & (data.time<=pd.to_datetime(yr[1]+'-12-31')),['byear']] = yr[0]
        data.loc[(data.time>=pd.to_datetime(yr[0]+'-1-1')) & (data.time<=pd.to_datetime(yr[1]+'-12-31')),['eyear']] = yr[1]

    # Now generates the specific data filenames.
    if len(models)==1:
        model = models[0]
        # Deal with special cases in filenames.
        if model=='CCSM4':
            version = '_r6i1p1_'
        else:
            version = '_r1i1p1_'
        data.ix[data.time < pd.to_datetime('2006-1-1'), 'filename'] = directory + 'macav2metdata_' + fvar + '_' + model + version + 'historical_' + data.byear + '_' + data.eyear + '_CONUS_daily.nc'
        data.ix[data.time >=pd.to_datetime('2006-1-1'), 'filename'] = directory + 'macav2metdata_' + fvar + '_' + model + version + 'rcp' + rcp + '_' + data.byear + '_' + data.eyear + '_CONUS_daily.nc'
        files = np.unique(data.filename)
        # print(files) # for testing
        for i,f in enumerate(files):
            maca      = xr.open_dataset(f)
            mdx = np.where((maca.variables['time']>=bdate.to_datetime64()) & (maca.variables['time']<=edate.to_datetime64()) )[0]
            if i==0:
                idx = data.index[ (data.time>=bdate) & (data.time<=maca.variables['time'][-1].values) ]
                data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
            elif i==len(files):
                idx = data.index[ (data.time>=maca.variables['time'][ 0].values) & (data.time<=edate.to_datetime64()) ]
                data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
            else:
                idx = data.index[ (data.time>=maca.variables['time'][ 0].values) & (data.time<=maca.variables['time'][-1].values) ]
                data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
            maca.close()

    else:
        for model in models:
            # Deal with special cases in filenames.
            if model=='CCSM4':
                version = '_r6i1p1_'
            else:
                version = '_r1i1p1_'
            data.ix[data.time < pd.to_datetime('2006-1-1'), 'filename'] = directory + 'macav2metdata_' + fvar + '_' + model + version + 'historical_' + data.byear + '_' + data.eyear + '_CONUS_daily.nc'
            data.ix[data.time >=pd.to_datetime('2006-1-1'), 'filename'] = directory + 'macav2metdata_' + fvar + '_' + model + version + 'rcp' + rcp + '_' + data.byear + '_' + data.eyear + '_CONUS_daily.nc'
            files = np.unique(data.filename)
            for i,f in enumerate(files):
                print(f)
                maca      = xr.open_dataset(f)
                mdx = np.where((maca.variables['time']>=bdate.to_datetime64()) & (maca.variables['time']<=edate.to_datetime64()) )[0]
                if i==0:
                    idx = data.index[ (data.time>=bdate) & (data.time<=maca.variables['time'][-1].values) ]
                    data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
                elif i==len(files):
                    idx = data.index[ (data.time>=maca.variables['time'][ 0].values) & (data.time<=edate.to_datetime64()) ]
                    data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
                else:
                    idx = data.index[ (data.time>=maca.variables['time'][ 0].values) & (data.time<=maca.variables['time'][-1].values) ]
                    data[model].ix[idx] = maca.variables[var][mdx, ilat, ilon]
                maca.close()

    finalData = pd.DataFrame({},index=data.time)
    for model in models:
        finalData[model] = data[model].values

    return finalData

