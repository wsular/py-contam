#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 15:02:54 2017

@author: Von P. Walden, Washington State University
"""

# Cincinnati
RH1    = pd.read_csv('/Users/vonw/data/iaq/maca/NKN/Cincinnati_Models1_4.5_RH_2006_2099.csv',skiprows=26,parse_dates=True,index_col='yyyy-mm-dd')
RH2    = pd.read_csv('/Users/vonw/data/iaq/maca/NKN/Cincinnati_Models2_4.5_RH_2006_2099.csv',skiprows=10,parse_dates=True,index_col='yyyy-mm-dd')
rhmax  = pd.DataFrame({'CNRM-CM5'     : RH1['rhsmax_CNRM-CM5_rcp45(%)'],
                       'GFDL-ESM2M'   : RH1['rhsmax_GFDL-ESM2M_rcp45(%)'],
                       'HadGEM2-ES365': RH1['rhsmax_HadGEM2-ES365_rcp45(%)'],
                       'IPSL-CM5A-LR' : RH1['rhsmax_IPSL-CM5A-LR_rcp45(%)'],
                       'MIROC-ESM'    : RH1['rhsmax_MIROC-ESM_rcp45(%)'],
                       'MIROC5'       : RH2['rhsmax_MIROC5_rcp45(%)']}, index=RH1.index)
rhmax['2009-12-31':'2020-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmax_4.5_2009_2020.csv')
rhmax['2049-12-31':'2060-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmax_4.5_2049_2060.csv')
rhmax['2029-12-31':'2040-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmax_4.5_2029_2040.csv')

rhmin  = pd.DataFrame({'CNRM-CM5'     : RH1['rhsmin_CNRM-CM5_rcp45(%)'],
                       'GFDL-ESM2M'   : RH1['rhsmin_GFDL-ESM2M_rcp45(%)'],
                       'HadGEM2-ES365': RH1['rhsmin_HadGEM2-ES365_rcp45(%)'],
                       'IPSL-CM5A-LR' : RH1['rhsmin_IPSL-CM5A-LR_rcp45(%)'],
                       'MIROC-ESM'    : RH1['rhsmin_MIROC-ESM_rcp45(%)'],
                       'MIROC5'       : RH2['rhsmin_MIROC5_rcp45(%)']}, index=RH1.index)
rhmin['2009-12-31':'2020-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmin_4.5_2009_2020.csv')
rhmin['2049-12-31':'2060-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmin_4.5_2049_2060.csv')
rhmin['2029-12-31':'2040-01-02'].to_csv('/Users/vonw/data/iaq/maca/Cincinnati_rhmin_4.5_2029_2040.csv')