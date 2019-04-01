# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 12:39:26 2019

@author: Von P. Walden, Washington State University
"""

from glob import glob

#years = (1996, 2000, 2004, 2088, 2092)
years = (2088, 2092)
d   = '/mnt/data/lima/iaq/contam/weatherFiles/'

for year in years:
    fns = glob(d + '*' + str(year) + '*.wth')
    fns.sort()
    for fn in fns:
        print('Processing: ' + fn)
        fi = open(fn,'r')
        fo = open(d + 'tmp/' + fn.split('/')[-1], 'w')
        lines = fi.readlines()
        fi.close()
        for line in lines:
            if(line.find('02/29')>=0):
                continue
            else:
                fo.write(line)
        fo.close()
