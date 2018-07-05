# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:41:45 2017

@author: Von P. Walden, Washington State University
"""

##IF 2/29 ignore.
##DST 0 - 1

import errno
import xarray as xr
import pandas as pd
import numpy as np
import os
from   datetime import datetime, timedelta
from math import *
import xarray as xr
import numpy  as np
import pandas as pd
from   datetime import datetime, timedelta
import sys

def find_WRF_pixel(latvar,lonvar,lat0,lon0):
    # Read latitude and longitude from file into numpy arrays
    # Renamed findWRFpixel from original function, naive_fast, written by Vikram Ravi.
    latvals = latvar[:]
    lonvals = lonvar[:]
    dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
    minindex_flattened = dist_sq.argmin()  # 1D index of min element
    iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
    return int(iy_min),int(ix_min)

def read_datafile(gridFile, dataFile, lat, lon, vrs, eqs):
    """
    This function reads data from a WRF CMAQ data file into a pandas dataframe, df.
    The dataframe can then be written to a CONTAM weather file using function,
    writeContamWeatherFile.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    2 Jun 2017
    """    
    # Open the WRF GRIDCRO2D file to determine the WRF pixel for lat/lon.
    print('reading ' + dataFile)
    GRID = xr.open_dataset(gridFile)
    ilat, ilon = find_WRF_pixel(GRID.LAT[0,0,:,:].values,GRID.LON[0,0,:,:].values,lat,lon)
    # Open WRF-CMAQ data file.
    print(dataFile)
    DATA = xr.open_dataset(dataFile)
    # Create a datetime index.
    datestr = str(DATA.SDATE)
    date    = datetime(int(datestr[0:4]),1,1) + timedelta(int(datestr[4:])-1)
    time    = [date + timedelta(hours=float(t)) for t in DATA.TSTEP]
    #
    # ............................... WEATHER DATA ............................
    #


        
    
    
    # Create a pandas dataframe with meteorological variables.
    wth   = pd.DataFrame({},index=time)
    wth = wth.set_index(pd.DatetimeIndex(wth.index))
    
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
            
        
        wth[vr] = dat
    #twenty_ninth = datetime.DateTime(, today.Month, today.Day, 10,)
    #
    # ........................... CONTAMINANT DATA ............................
    #
    # Read contaminat data from WRF-CMAQ data file.
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
        weather   = pd.DataFrame({'Ta':T, 
                             'Pb':P,
                             'Ws':wspd,
                             'Wd':wdir,
                             'Hr':w},
                             index=time)
        return wth, weather
        #filename = dataFile.split('/')[-1]
        #filestr = '{}.weather.ctm'.format(filename)
        #writeContamWeatherFile(filestr,weather)
    
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


def writeContamSpeciesFile(specFile, df):
    """
    This function writes the data in the pandas dataframe, df, to a text file.
    The text file is formatted as a CONTAM species file.

    """
    # Open new weather file.
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
    
    # Close the weather file.
    fp.close()
    
    return

def process_datafiles(grid_path, extr_path, out_path, sites_path, vars_path, year, output_dir):
    vrs = pd.read_csv(vars_path)
    sites = pd.read_csv(sites_path)
    sites = sites.dropna(subset=['City_Name'])
    extrs = [extr_path+x for x in os.listdir(extr_path)]
    outs = [out_path+x for x in os.listdir(out_path)]

    extr_frm = vrs[vrs['Location']=='Extr']
    out_frm = vrs[vrs['Location']=='Out']
    
    extr_vrs =extr_frm['Name']
    out_vrs =out_frm['Name']
    print(vrs)
    
    extr_eqs = extr_frm['Convert units']
    out_eqs = out_frm['Convert units']
    
    lats = sites.Latitude.values.tolist()
    lons = sites.Longitude.values.tolist()
    names = sites.City_Name.values.tolist()
    

    for x in range(len(lats)):
        lat = lats[x]
        lon = lons[x]
        name = names[x]
        try:
            os.mkdir(output_dir+name)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
        mydir = output_dir + name + "/"
        
        all_exts = []
        all_outs = []
        all_weathers = []
        for out in outs:
            out = read_datafile(grid_path,out,lat,lon,out_vrs, out_eqs)
            all_outs.append(out)            
        for extr in extrs:
            ext, weather = read_datafile(grid_path,extr,lat,lon, extr_vrs, extr_eqs)
            all_exts.append(ext)
            all_weathers.append(weather)
            
        all_outs_frame = pd.concat(all_outs)
        all_exts_frame = pd.concat(all_exts)
        all_weathers_frame = pd.concat(all_weathers)

        all_weathers_frame = all_weathers_frame.sort_index()
        
        comb = all_exts_frame.join(all_outs_frame, how="outer")
        
        
        
        filestr = year + '_rcp4.5_' + name
        writeContamSpeciesFile(mydir + filestr+'.ctm',comb)
        writeContamWeatherFile(mydir + filestr+'.wth',all_weathers_frame)
        print('wrote {}.ctm and weather file'.format(filestr))
        
def process_datafiles_2(grid_path, extr_path, out_path, sites_path, vars_path, year, output_dir,site_id):
    vrs = pd.read_csv(vars_path)

    sites = pd.read_csv(sites_path)
    sites = sites.dropna(subset=['City_Name'])
    extrs = [extr_path+x for x in os.listdir(extr_path)]
    outs = [out_path+x for x in os.listdir(out_path)]

    extr_frm = vrs[vrs['Location']=='Extr']
    out_frm = vrs[vrs['Location']=='Out']
    print(vrs)
    
    extr_vrs =extr_frm['Name']
    out_vrs =out_frm['Name']
    
    extr_eqs = extr_frm['Convert units']
    out_eqs = out_frm['Convert units']
    
    lats = sites.Latitude.values.tolist()
    lons = sites.Longitude.values.tolist()
    names = sites.City_Name.values.tolist()
    
    lat = lats[site_id]
    lon = lons[site_id]
    name = names[site_id]
    
    try:
        os.mkdir(output_dir+name)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise
        pass
    mydir = output_dir + name + "/"
    
    all_exts = []
    all_outs = []
    all_weathers = []
    for out in outs:
        out = read_datafile(grid_path,out,lat,lon,out_vrs, out_eqs)
        all_outs.append(out)            
    for extr in extrs:
        ext, weather = read_datafile(grid_path,extr,lat,lon, extr_vrs, extr_eqs)
        all_exts.append(ext)
        all_weathers.append(weather)
        
    all_outs_frame = pd.concat(all_outs)
    all_exts_frame = pd.concat(all_exts)
    all_weathers_frame = pd.concat(all_weathers)

    all_weathers_frame = all_weathers_frame.sort_index()
    
    comb = all_exts_frame.join(all_outs_frame, how="outer")
    
    filestr = year + '_rcp4.5_' + name
    writeContamSpeciesFile(mydir + filestr+'.ctm',comb)
    writeContamWeatherFile(mydir + filestr+'.wth',all_weathers_frame)
    print('wrote {}.ctm and weather file'.format(filestr))

def testMain():
    grid_path = './lima.grid'
    extr_dir = './extr/'
    out_dir = './out/'
    sites_path = './sites.csv'
    vars_path = './vrs.csv'
    
    output_dir = '/home/ktoombs/Downloads/nath/newoutput/'
    
    return process_datafiles(grid_path, extr_dir, out_dir, sites_path, vars_path, '2048', output_dir)

def serverMain():
    extr_dir = '/mnt/data/lima/iaq/cmaq/extr/rcp8.5/'
    out_dir = '/mnt/data/lima/iaq/cmaq/out/rcp8.5/'
    grid_path = '/mnt/data/lima/iaq/cmaq/GRIDCRO2D_19941215'
    sites_path = '/mnt/data/lima/iaq/cmaq/sites.csv'
    vars_path = '/mnt/data/lima/iaq/cmaq/vrs.csv'
    
    output_dir = '/mnt/data/lima/iaq/cmaq/rcp_8.5_out/'
    
    years = ['2045','2046','2047','2048','2049','2050','2051','2052','2053','2054','2055']
    for year in years:
        process_datafiles(grid_path, extr_dir+year+"/", out_dir+year+"/", sites_path, vars_path, year, output_dir)

def partial(year, siteid):
    grid_path = './lima.grid'
    extr_dir = './extr/'
    out_dir = './out/'
    sites_path = './sites.csv'
    vars_path = './vrs.csv'
    
    output_dir = '/home/ktoombs/Downloads/nath/newoutput/'
    
    process_datafiles_2(grid_path, extr_dir, out_dir, sites_path, vars_path, year, output_dir, siteid)

def partial_server(year, siteid):
    extr_dir = '/data/lar/users/lima/cmaq/extr/rcp4.5/'
    out_dir = '/data/lar/users/lima/cmaq/out/rcp4.5/'
    grid_path = '/data/lar/users/lima/cmaq/GRIDCRO2D_19941215'
    sites_path = '/home/lima/iaq/input/sites.csv'
    vars_path = '/home/lima/iaq/input/vrs.csv'
    
    output_dir = '/home/ktoombs/'
    
    process_datafiles_2(grid_path, extr_dir+year+'/', out_dir+year+'/', sites_path, vars_path, year, output_dir, siteid)

if __name__=='__main__':
    #testMain()
    serverMain()
    #partial(sys.argv[1],int(sys.argv[2]))
    #partial_server(sys.argv[1], int(sys.argv[2]))
    pass

