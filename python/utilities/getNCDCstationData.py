# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 20:10:05 2018

@author: Von P. Walden, Washington State University
"""
import pandas as pd


def NCDCstationData(USAF, WBAN, BYR, EYR):
    """ Input:
            USAF - USAF station code obtained from isd-history.csv (as int)
            WBAN - WBAN station code obtained from isd-history.csv (as int)
            BYR  - Beginning year (as int)
            EYR  - Endind year (as int)
    """
    from os         import chdir
    from subprocess import call
    chdir('/Volumes/vonw/data/iaq/NCDC/ish/')
    FTP = 'ftp://ftp.ncdc.noaa.gov//pub/data/noaa/'
    for date in pd.date_range(str(BYR),str(EYR+1),freq='A'):
        YEAR = date.year
        wget_str = FTP + str(YEAR) + '/' + str(USAF) + '-' + str(WBAN) + '-' + str(YEAR) + '.gz'
        call(['wget', wget_str])
    return
 
isd = pd.read_csv('/Users/vonw/work/software/iaq/2015-iaq-contam-input/documentation/isd-history-IAQ.csv')
BYR = 2003
EYR = 2012

for USAF, WBAN in zip(isd.USAF,isd.WBAN):
    NCDCstationData(USAF, WBAN, BYR, EYR)
    
