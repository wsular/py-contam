# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 13:21:14 2018

@author: Von P. Walden, Washington State University
"""
import os
import pandas as pd
from glob import glob
from subprocess import call

site_data = pd.read_csv('/mnt/data/lima/iaq/cmaq/sites.csv')

for row, city in site_data.iterrows():
    if city['City_Name'] == " ": continue
    
    for rcp in ["4.5", "8.5"]:
        rcpdir   = '/mnt/data/lima/iaq/cmaq/prj' + rcp + '/' + city['City_Name'] + '/'
        os.chdir(rcpdir)
        prjFiles = glob(rcpdir+'*.prj')
        prjFiles.sort()
        
        for prjFile in prjFiles[0:10]:
            call(['/mnt/data/lima/contam/contam-x-3.2-gcc.exe',prjFile])
