#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 09:15:41 2017

@author: ktoombs
"""
import os
import pandas as pd
name = []
csvs = []

outdir = '/mnt/data/lima/iaq/aqs/mid_files/'
sites = '/mnt/data/lima/iaq/aqs/sites.csv'

sitesframe = pd.read_csv(sites)
lats = sitesframe.Latitude.values
lons = sitesframe.Longitude.values
longnums = sitesframe.AQS_Site_ID.values

year = '2005'
data_path = '/mnt/data/lima/iaq/aqs/'
#years = '05','06','07','08','09','10','11','12','13','14','15','16'
years2 = '2005'
x = 0

def main():
    x = 0
    for year in years2:
        for file in os.listdir(data_path):
            joined = os.path.join(data_path, file)
            if(os.path.isdir(joined)):
                for var_name in os.listdir(joined):
                    joined2 = os.path.join(joined, var_name)
                    if(os.path.isdir(joined2)):
                        print(var_name, len(os.listdir(joined2)))
                        for hourly_folder in os.listdir(joined2):
                            joined3 = os.path.join(joined2, hourly_folder)
                            for hourly_file in os.listdir(joined3):
                                if (hourly_file.endswith('.csv')):
                                    print(hourly_file)
                                    newpath = os.path.join(joined3, hourly_file)
                                    print(newpath)

                                    df = pd.read_csv(newpath)
                                    x = 0
                                    for lat, lon, longnum in zip(lats, lons, longnums):
                                        a= longnum[0:2]
                                        b= longnum[3:6]
                                        c= longnum[7:11]
                                        a = int(a.lstrip('0'))
                                        b = int(b.lstrip('0'))
                                        c = int(c.lstrip('0'))
                                        
                                        df['State Code'].dtype
                                        df2 = df[df['State Code'] == a]
                                        df2 = df2[df2['County Code'] == b]
                                        df2 = df2[df2['Site Num'] == c]
                                        
                                        yeardd = hourly_file[-8:-4]
                                        
                                        df2.to_csv(outdir+str(x)+"_"+yeardd+"_"+var_name+'.csv')
                                        '''
                                        print(outdir+str(x)+"_"+yeardd+"_"+var_name+'.csv')
                                        '''
                                        x = x + 1
                                        


main()
