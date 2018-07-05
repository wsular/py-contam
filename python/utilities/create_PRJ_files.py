# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 12:03:52 2018

@author: Von P. Walden, Washington State University
"""

import pandas as pd
from glob import glob

years     = range(2045,2056)
houses    = glob('/mnt/data/lima/iaq/home_models/*.prj')
site_data = pd.read_csv('/mnt/data/lima/iaq/cmaq/sites.csv')
models    = ['CCSM4', 'CNRM-CM5', 'GFDL-ESM2M', 'HadGEM2-ES365', 'IPSL-CM5A-LR', 'MIROC5', 'MIROC-ESM' ]

for row, city in site_data.iterrows():
    if city['City_Name'] == " ": continue
    
    for yr in years:
        year = str(yr)
        
        for rcp in ["4.5", "8.5"]:
            rcpdir = '/mnt/data/lima/iaq/cmaq/rcp_' + rcp + '_out/' + city['City_Name']
            outdir = '/mnt/data/lima/iaq/cmaq/prj' + rcp + '/' + city['City_Name'] + '/'
            
            for model in models:
                for house in houses:
                    # Read in contam project file template.
                    lines   = open(house, 'r').readlines()
                    prjFile = list(lines)
                    # Determine paths to weather and contaminant files
                    wthpath = rcpdir + '/' + city['City_Name'] + '_' + year + '_' + rcp + '_' + model + '.wth'
                    ctmpath = rcpdir + '/' + year + '_rcp' + rcp + '_' + city['City_Name'] + '.ctm'
                    # Replace lines in template with desired information.
                    prjFile[9]  = wthpath + ' ! weather file\n'
                    prjFile[10] = ctmpath + ' ! contaminant file\n'
                    prjFile[21] = ' {:>6} {:>6} {:>6} {:>6} 283.15 2 0\n'.format(city['Latitude'], city['Longitude'],city['tznr'],city['altd'])
                    prjFile[38] = ('  Jan01 00:00:00  Jan01 00:00:00  Dec31 23:00:00  01:00:00 01:00:00 01:00:00\n')
                    # Write new contam project file
                    with open(outdir+house.split('/')[-1]+ctmpath.split('/')[-1]+wthpath.split('/')[-1]+'.prj','w') as out: out.writelines(prjFile)
