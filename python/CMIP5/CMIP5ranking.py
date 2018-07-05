# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 15:05:24 2017

@author: Von P. Walden, Washington State University
"""
#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%
cmip5 = pd.read_csv('/Users/vonw/work/projects/iaq/analysis/maca/CMIP5_bias_SheffieldEtAl_2013.csv')

plt.figure()
plt.plot(cmip5.index+1,cmip5['Winter Precipitation Bias'],'o')
plt.plot(cmip5.index+1,cmip5['Summer Precipitation Bias'],'o')
plt.plot(cmip5.index+1,cmip5['Winter Temperature Bias']/cmip5['Winter Temperature Bias'].mean(),'o')
plt.plot(cmip5.index+1,cmip5['Summer Temperature Bias']/cmip5['Summer Temperature Bias'].mean(),'o')
plt.grid()
plt.axis([0,18,-40,40])
plt.legend(('Winter Precip','Summer Precip','Winter Temp','Summer Temp'),loc='best')
plt.show()

#%%
cmip5['Absolute Bias'] = np.nan
for i in cmip5.index:
#    cmip5.iloc[i]['Absolute Bias'] = array([abs(cmip5.iloc[i]['Winter Precipitation Bias']),
#                                            abs(cmip5.iloc[i]['Summer Precipitation Bias']),
#                                            abs(cmip5.iloc[i]['Winter Temperature Bias']/cmip5['Winter Temperature Bias'].mean()),
#                                            abs(cmip5.iloc[i]['Summer Temperature Bias']/cmip5['Summer Temperature Bias'].mean())]).mean()
    print(cmip5.iloc[i].Model,"\t",np.array([abs(cmip5.iloc[i]['Winter Precipitation Bias']),
                                            abs(cmip5.iloc[i]['Summer Precipitation Bias']),
                                            abs(cmip5.iloc[i]['Winter Temperature Bias']/cmip5['Winter Temperature Bias'].mean()),
                                            abs(cmip5.iloc[i]['Summer Temperature Bias']/cmip5['Summer Temperature Bias'].mean())]).mean())
    
# Top 10 model rankings for ability to collectively match historical observations of
#   Winter precipitation
#   Summer precipitation
#   Winter temperature
#   Summer temperature
#
# 1)  CNRM-CM5
# 2)  CCSM4
# 3)  IPSL-CM5A-LR
# 4)  MIROC5
# 5)  NorESM1-M
# 6)  (?) HadCM3
# 7)  MIROC-ESM
# 8)  (?) MPI-ESM-LR
# 9)  GFDL-ESM2M
# 10) HadGEM2-ES