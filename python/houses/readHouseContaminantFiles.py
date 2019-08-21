#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 19:22:52 2019

@author:    Von P. Walden
            Washington State University
"""

import pandas as pd

ds  = ['/Users/vonw/data/iaq/houses/outdoors/h005_outdoor_summer/']
fns = ['outdoor_rack-Table 1.csv', 
       'PM2.5-Table 1.csv', 
       'PTR-MS-Table 1.csv']

d  = ds[0]
fn = fns[0]

df = pd.read_csv(d+fn, header=[0], 
                 skiprows=[1], 
                 parse_dates=True, 
                 index_col=[0], 
                 skipinitialspace=True)
units = pd.read_csv(d+fn, nrows=1).values[0]

