# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 14:50:43 2016

@author: Von P. Walden, Washington State University
"""

# Run on aeolus.
#from maca_aeolus import maca
#fvar          = 'tasmax'
#models        = ['bcc-csm1-1','BNU-ESM','CanESM2','CCSM4','CNRM-CM5','CSIRO-Mk3-6-0','GFDL-ESM2G','GFDL-ESM2M','HadGEM2-CC365','HadGEM2-ES365','inmcm4','IPSL-CM5A-LR','IPSL-CM5A-MR','IPSL-CM5B-LR','MIROC-ESM','MIROC-ESM-CHEM','MIROC5','MRI-CGCM3','NorESM1-M']
#rcp           = 4.5
#latitude      = 46.7
#longitude     = 242.8
#hist          = maca(fvar,models,rcp,'1950-1-1','2005-12-31',latitude,longitude)
#T2030s        = maca(fvar,models,rcp,'2030-1-1','2039-12-31',latitude,longitude)
#T2050s        = maca(fvar,models,rcp,'2050-1-1','2059-12-31',latitude,longitude)
#hist.to_csv('Tmax_historical.csv')
#T2030s.to_csv('Tmax_rcp45_2030s.csv')
#T2050s.to_csv('Tmax_rcp45_2050s.csv')

hist   = pd.read_csv('/Users/vonw/Desktop/hist.csv')
hist   = pd.DataFrame(hist.iloc[:,1:].values,index=hist.time,columns=hist.columns[1:])
T2030s = pd.read_csv('/Users/vonw/Desktop/Tmax_rcp45_2030s.csv')
T2030s = pd.DataFrame(T2030s.iloc[:,1:].values,index=T2030s.time,columns=T2030s.columns[1:])
T2050s = pd.read_csv('/Users/vonw/Desktop/Tmax_rcp45_2050s.csv')
T2050s = pd.DataFrame(T2050s.iloc[:,1:].values,index=T2050s.time,columns=T2050s.columns[1:])

fig, ax = plt.subplots(1, 1)
hist.plot.box(  ax=ax,color=dict(boxes='Blue', whiskers='Blue', medians='Blue', caps='Blue'), sym='b+', title='Climate Change Simulations (rcp4.5) for Pullman, WA')
T2030s.plot.box(ax=ax,color=dict(boxes='Green',whiskers='Green',medians='Green',caps='Green'),sym='g+')
T2050s.plot.box(ax=ax,color=dict(boxes='Red',  whiskers='Red',  medians='Red',  caps='Red'),  sym='r+')
ax.set_xticklabels(hist.columns, rotation=270, fontsize=8)
ax.set_ylabel('Temperature (K)')
grid()
plot(list(range(1,20)),hist.mean(),  'bo-')
plot(list(range(1,20)),T2030s.mean(),'go-')
plot(list(range(1,20)),T2050s.mean(),'ro-')
