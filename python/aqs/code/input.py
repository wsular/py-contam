# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:41:45 2017

@author: Von P. Walden, Washington State University
"""

def readWRF_CMAQ(gridFile, dataFile, lat, lon):
    """
    This function reads data from a WRF CMAQ data file into a pandas dataframe, df.
    The dataframe can then be written to a CONTAM weather file using function,
    writeContamWeatherFile.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    2 Jun 2017
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
        
    # Open the WRF GRIDCRO2D file to determine the WRF pixel for lat/lon.
    GRID = xr.open_dataset(gridFile)
    ilat, ilon = find_WRF_pixel(GRID.LAT[0,0,:,:].values,GRID.LON[0,0,:,:].values,lat,lon)
    
    # Open WRF-CMAQ data file.
    DATA = xr.open_dataset(dataFile)
    # Create a datetime index.
    datestr = str(DATA.SDATE)
    date    = datetime(int(datestr[0:4]),1,1) + timedelta(int(datestr[4:])-1)
    time    = [date + timedelta(hours=float(t)) for t in DATA.TSTEP]
    #
    # ............................... WEATHER DATA ............................
    #
    # Read meteorological data from WRF-CMAQ data file.
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
    #
    # ........................... CONTAMINANT DATA ............................
    #
    # Read contaminat data from WRF-CMAQ data file.

    return wth

def writeContamWeatherFile(wthrFile, df):
    """
    This function writes the data in the pandas dataframe, df, to a text file.
    The text file is formatted as a CONTAM weather file.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    2 Jun 2017
    """
    # Open new weather file.
    fp = open(wthrFile, 'w')
    
    # Write the first header lines.
    fp.write('WeatherFile ContamW 2.0\n\n');
    fp.write(df.index[0].to_pydatetime().strftime('%m/%d')  + '	 !start-of-file date\n');
    fp.write(df.index[-1].to_pydatetime().strftime('%m/%d') + '	 !end-of-file date\n');
    fp.write('!Date	DofW	Dtype	DST	Tgrnd [K]\n');
    
    # Write daily average data.
    dfa = df.resample('1D').mean()
    for day in dfa.index:
        fp.write(  day.strftime('%m/%d') + '\t' 
                 + str(day.weekday()+1)     + '\t'
                 + str(day.weekday()+1)     + '\t'
                 + '1'                      + '\t'
                 + str(dfa.loc[day]['Ta'])  + '\n')
            
    # Write the second header line.
    fp.write('!Date	Time	Ta [K]	Pb [Pa]	Ws [m/s]	Wd [deg]	Hr [g/kg]	Ith [kJ/m^2]	Idn [kJ/m^2]	Ts [K]	Rn [-]	Sn [-]\n');

    # Write the hourly data.
    for hour in df.index:
        fp.write(  hour.strftime('%m/%d') + '\t'
                 + hour.strftime('%H:%M:%S') + '\t'
                 + str(df.loc[hour]['Ta'])   + '\t'
                 + str(df.loc[hour]['Pb'])   + '\t'
                 + str(df.loc[hour]['Ws'])   + '\t'
                 + str(df.loc[hour]['Wd'])   + '\t'
                 + str(df.loc[hour]['Hr'])   + '\t'
                 + '0'                       + '\t'
                 + '0'                       + '\t'
                 + '0'                       + '\t'
                 + '0'                       + '\t'
                 + '0'                       + '\n')
    
    # Close the weather file.
    fp.close()
    
    return
