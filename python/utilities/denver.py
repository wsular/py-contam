# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:50:22 2018

@author: Von P. Walden, Washington State University
"""

import contam
from   glob   import glob

## Denver
files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj4.5/Denver/*.sim')
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

files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj8.5/Denver/*.sim')
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

# Process the indoor contaminants by reading each contaminant node and
#   extracting the contaminants (ozone and PM2.5) and averaging them.
o3_45 = ctm45.copy(deep=True)
for col in o3_45:
    o3_45[col] = np.array([data[1][20] for data in ctm45[col].iteritems()])
iO3_45 = o3_45.mean(axis=1) * 1e9*28.97/48  # Convert to ppb
oO3_45 = amb45.Ctm21        * 1e9*28.97/48

o3_85 = ctm85.copy(deep=True)
for col in o3_85:
    o3_85[col] = np.array([data[1][20] for data in ctm85[col].iteritems()])
iO3_85 = o3_85.mean(axis=1) * 1e9*28.97/48  # Convert to ppb
oO3_85 = amb85.Ctm21        * 1e9*28.97/48

figure()
subplot(121)
iO3_45.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='gray')
oO3_45.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='green' )
axis([0,90,0,0.04])
xlabel('Ozone, ppb')
title('Denver, CO: RCP4.5')
#legend(('indoor','outdoor'))
subplot(122)
iO3_85.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='gray')
oO3_85.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='green')
axis([0,90,0,0.04])
xlabel('Ozone, ppb')
title('RCP8.5')
legend(('indoor','outdoor'))



## Boston
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

# Process the indoor contaminants by reading each contaminant node and
#   extracting the contaminants (ozone and PM2.5) and averaging them.
o3_45 = ctm45.copy(deep=True)
for col in o3_45:
    o3_45[col] = np.array([data[1][20] for data in ctm45[col].iteritems()])
iO3_45 = o3_45.mean(axis=1) * 1e9*28.97/48  # Convert to ppb
oO3_45 = amb45.Ctm21        * 1e9*28.97/48

o3_85 = ctm85.copy(deep=True)
for col in o3_85:
    o3_85[col] = np.array([data[1][20] for data in ctm85[col].iteritems()])
iO3_85 = o3_85.mean(axis=1) * 1e9*28.97/48  # Convert to ppb
oO3_85 = amb85.Ctm21        * 1e9*28.97/48

figure()
subplot(121)
iO3_45.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='gray')
oO3_45.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='green' )
axis([0,90,0,0.04])
xlabel('Ozone, ppb')
title('Denver, CO: RCP4.5')
#legend(('indoor','outdoor'))
subplot(122)
iO3_85.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='gray')
oO3_85.plot.hist(bins=arange(0,90,1),normed=True,alpha=0.5,color='green')
axis([0,90,0,0.04])
xlabel('Ozone, ppb')
title('RCP8.5')
legend(('indoor','outdoor'))






o3_85 = ctm85.copy(deep=True)
for col in o3_85:
    o3_85[col] = np.array([data[1][20] for data in ctm85[col].iteritems()])
iO3_85 = o3_85.mean(axis=1) * 1e9*28.97/48  # Convert to ppb
oO3_85 = amb85.Ctm21        * 1e9*28.97/48

figure()
(Denver45.Tambt-273.15).plot.hist(bins=arange(-30,45,1),normed=True,color='blue',alpha=0.7)
(Denver85.Tambt-273.15).plot.hist(bins=arange(-30,45,1),normed=True,color='red', alpha=0.7)
axis([-30,45,0,0.035])
xlabel('Temperature, C')
title('Denver, CO: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
Denver45.Ws.plot.hist(bins=arange(0,15,1),normed=True,color='blue',alpha=0.7)
Denver85.Ws.plot.hist(bins=arange(0,15,1),normed=True,color='red', alpha=0.7)
axis([0,15,0,0.25])
xlabel('Wind speed, m s-1')
title('Denver, CO: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
ozone45 = amb45.Ctm21*1e9*28.97/48
ozone85 = amb85.Ctm21*1e9*28.97/48
ozone45.plot.hist(bins=arange(0,80,1),normed=True,color='blue',alpha=0.7)
ozone85.plot.hist(bins=arange(0,80,1),normed=True,color='red', alpha=0.7)
axis([0,80,0,0.04])
xlabel('Ozone Concentration, ppb')
title('Denver, CO: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
Denver45.Ctm37.plot.hist(normed=True,color='blue',alpha=0.7)
Denver85.Ctm37.plot.hist(normed=True,color='red', alpha=0.7)
#axis([0,100,0,0.5])
xlabel('PM2.5, ?????')
title('Denver, CO: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

## Boston
files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj4.5/Boston/*.sim')
files.sort()
amb45 = pd.DataFrame({})
for file in files[0:3]:
    print('Processing: ',file)
    sim      = contam.Contam(file)
    df       = sim.readAmbient()
    # Correct the time scale of the DataFrame.
    year     = int(file[file.rfind('prj')+3:file.rfind('prj')+7])
    df.index = df.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    amb45    = pd.concat([amb45, df])

files = glob('/Volumes/vonw/data/iaq/contam/cmaq/prj8.5/Boston/*.sim')
files.sort()
rcp85 = pd.DataFrame({})
for file in files[0:3]:
    print('Processing: ',file)
    sim      = contam.Contam(file)
    df       = sim.readAmbient()
    # Correct the time scale of the DataFrame.
    year     = int(file[file.rfind('prj')+3:file.rfind('prj')+7])
    df.index = df.index + (pd.datetime(year,1,1) - pd.datetime(1900,1,1))
    rcp85    = pd.concat([rcp85, df])

figure()
(rcp45.Tambt-273.15).plot.hist(bins=arange(-30,45,1),normed=True,color='blue',alpha=0.7)
(rcp85.Tambt-273.15).plot.hist(bins=arange(-30,45,1),normed=True,color='red', alpha=0.7)
axis([-30,45,0,0.05])
xlabel('Temperature, C')
title('Boston, MA: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
rcp45.Ws.plot.hist(bins=arange(0,15,1),normed=True,color='blue',alpha=0.7)
rcp85.Ws.plot.hist(bins=arange(0,15,1),normed=True,color='red', alpha=0.7)
axis([0,15,0,0.25])
xlabel('Wind speed, m s-1')
title('Boston, MA: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
ozone45 = amb45.Ctm21*1e9*28.97/48
ozone85 = amb85.Ctm21*1e9*28.97/48
ozone45.plot.hist(bins=arange(0,80,1),normed=True,color='blue',alpha=0.7)
ozone85.plot.hist(bins=arange(0,80,1),normed=True,color='red', alpha=0.7)
axis([0,80,0,0.04])
xlabel('Ozone Concentration, ppb')
title('Boston, MA: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')

figure()
rcp45.Ctm37.plot.hist(color='blue',alpha=0.7)
rcp85.Ctm37.plot.hist(color='red', alpha=0.7)
#axis([0,100,0,0.5])
xlabel('PM2.5, ?????')
ylabel('Number of Occurrences')
title('Boston, MA: 2045-2047')
legend(('RCP4.5','RCP8.5'),loc='best',facecolor='white')
