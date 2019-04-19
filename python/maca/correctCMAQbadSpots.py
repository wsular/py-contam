# -*- coding: utf-8 -*-
"""
Created on Tue Apr 16 16:25:17 2019

@author: Von P. Walden, Washington State University
"""
import pandas as pd
from glob import glob

# Bad time periods in CMAQ files from EPA
# ....1996 - 2005
#times = pd.date_range('1997-02-13 06:00', 
#                      '1997-02-14 00:00', freq='H')
#times = pd.date_range('1998-10-15 13:00', 
#                      '1998-10-16 00:00', freq='H')
#times = pd.date_range('2004-03-19 01:00', 
#                      '2004-03-20 00:00', freq='H')
#times = pd.date_range('2004-05-14 22:00', 
#                      '2004-05-15 00:00', freq='H')
times = pd.date_range('2004-05-15 23:00', 
                      '2004-05-17 00:00', freq='H')
#times = pd.date_range('2004-10-26 19:00', 
#                      '2004-10-27 00:00', freq='H')

year  = times[0].year
d     = '/mnt/data/lima/iaq/contam/contaminantFiles/'

fns = glob(d + '*' + str(year) + '*.ctm')
fns.sort()
for fn in fns:
    print('Processing: ' + fn)
    fi = open(fn,'r')
    lines = fi.readlines()
    fi.close()
    fo = open(d + 'tmp/' + fn.split('/')[-1], 'w')
    # Decodes lines to use for linear interpolation.
    bline = [line for line in lines if(line.find(times[0].strftime('%m/%d\t%H:%M'))>=0)][0]
    eline = [line for line in lines if(line.find(times[-1].strftime('%m/%d\t%H:%M'))>=0)][0]
    FORM0 = np.float(bline.split('\t')[2])
    FORM1 = np.float(eline.split('\t')[2])
    FORM  = np.poly1d(np.polyfit([times[0].value, times[-1].value], [FORM0, FORM1],1))
    O30   = np.float(bline.split('\t')[3])
    O31   = np.float(eline.split('\t')[3])
    O3    = np.poly1d(np.polyfit([times[0].value, times[-1].value], [O30, O31],1))
    PM250 = np.float(bline.split('\t')[4])
    PM251 = np.float(eline.split('\t')[4])
    PM25  = np.poly1d(np.polyfit([times[0].value, times[-1].value], [PM250, PM251],1))
    # Lines before bad spot.
    for linenum, line in enumerate(lines):
        if(line.find(times[1].strftime('%m/%d\t%H:%M'))<0):
            fo.write(line)
        else:
            break
    # Write interpolated values over bad spot.
    for time in times[1:-1]:
        fo.write(time.strftime('%m/%d\t%H:%M:%S') + '\t' + str(FORM(time.value)) + '\t' + str(O3(time.value)) + '\t' + str(PM25(time.value)) + '\n')
    # Lines after bad spot.
    for line in lines[(linenum + len(times)-2):]:
        fo.write(line)
    fo.close()
