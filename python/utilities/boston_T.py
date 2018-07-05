# -*- coding: utf-8 -*-
"""
Created on Fri Feb  2 09:00:35 2018

@author: Von P. Walden, Washington State University
"""

import contam
from   glob   import glob

## Denver
files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj4.5/Boston/*.sim')
files.sort()
amb45 = pd.DataFrame({})
ctm45 = pd.DataFrame({})
for file in files[0:3]:
    print('Processing: ',file)
    sim      = contam.Contam(file)
    amb      = sim.readAmbient()
    ctm      = sim.readContaminantNodes()
    # Correct the time scale of the DataFrame.
    year     = int(file[file.rfind('prj')+3:file.rfind('prj')+7])
    amb.index= amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    amb45    = pd.concat([amb45, amb])
    # Correct the time scale of the DataFrame.
    ctm.index= ctm.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    ctm45    = pd.concat([ctm45, ctm])

files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj8.5/Boston/*.sim')
files.sort()
amb85 = pd.DataFrame({})
ctm85 = pd.DataFrame({})
for file in files[0:3]:
    print('Processing: ',file)
    sim      = contam.Contam(file)
    amb      = sim.readAmbient()
    ctm      = sim.readContaminantNodes()
    # Correct the time scale of the DataFrame.
    year     = int(file[file.rfind('prj')+3:file.rfind('prj')+7])
    amb.index= amb.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    amb85    = pd.concat([amb85, amb])
    # Correct the time scale of the DataFrame.
    ctm.index= ctm.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    ctm85    = pd.concat([ctm85, ctm])

from contam_input import readNOAA_ISH
df2005 = readNOAA_ISH("725650","03017",2005)
df2006 = readNOAA_ISH("725650","03017",2006)
df2007 = readNOAA_ISH("725650","03017",2007)
boston = pd.concat([df2005,df2006,df2007])

figure()
(boston.Ta-273.15).plot.hist(bins=arange(-20,45,1),normed=True,alpha=0.5,  color='blue')
(amb85.Tambt-273.15).plot.hist(bins=arange(-20,45,1),normed=True,alpha=0.5,color='red')
axis([-20,45,0,0.045])
xlabel('Temperature, C')
title('Air Temperature, Boston, MA')
legend(('2005-2007','2045-2047: RCP8.5'))
