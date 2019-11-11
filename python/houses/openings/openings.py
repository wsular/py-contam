#%%
"""
Created on Tue Jul 16 21:28:51 2019

@author:    Von P. Walden
            Washington State University
"""
from glob import glob
import pandas as pd
import numpy  as np

from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.plotting import figure

d = '/Users/vonw/data/iaq/houses/SmartHome/YiBo_UTC_WD_CleanedJitter/Atmo5SandW/'
fns = glob(d + '*.txt')

#%%
# Read all data files
houses = pd.read_csv('houseDates.csv', parse_dates=['StartDate','EndDate'])
df = pd.DataFrame(pd.read_csv(fns[0], sep='\t', names=['time', 'opening', 'state'], parse_dates=[0]))
for fn in fns:
    print(fn)
    df = pd.concat([df, pd.read_csv(fn, sep='\t', names=['time', 'opening', 'state'], parse_dates=[0])])
df.index = df.time
df.drop(columns=['time'], inplace=True)
df = df.sort_index()
df['code'] = np.nan
df['code'].loc[df['state']=='CLOSE'] = 0
df['code'].loc[df['state']=='OPEN']  = 1

#%%
from bokeh.palettes import brewer
colors = brewer['Set3'][12]

output_file(d + 'doors.html')
p1 = figure(plot_width=1000,
            plot_height=600,
            x_axis_type='datetime',
            title='Door Openings for ' + d.split('/')[-2])
#p1.step(df.index[df['opening']=='MainDoor'], df['code'][df['opening']=='MainDoor'], legend='MainDoor', color=colors[0])
p1.step(df.index[df['opening']=='DoorA'], df['code'][df['opening']=='DoorA'], legend='DoorA', color=colors[0])
p1.step(df.index[df['opening']=='DoorB'], df['code'][df['opening']=='DoorB'], legend='DoorB', color=colors[1])
p1.step(df.index[df['opening']=='DoorC'], df['code'][df['opening']=='DoorC'], legend='DoorC', color=colors[2])
p1.step(df.index[df['opening']=='DoorD'], df['code'][df['opening']=='DoorD'], legend='DoorD', color=colors[3])
p1.step(df.index[df['opening']=='DoorE'], df['code'][df['opening']=='DoorE'], legend='DoorE', color=colors[4])
#p1.step(df.index[df['opening']=='GarageDoor'], df['code'][df['opening']=='GarageDoor'], legend='GarageD', color=colors[4])
#p1.step(df.index[df['opening']=='EntrywayB'], df['code'][df['opening']=='EntrywayB'], legend='EntrywayB', color=colors[4])
#p1.step(df.index[df['opening']=='EntrywayC'], df['code'][df['opening']=='EntrywayC'], legend='EntrywayC', color=colors[5])
show(p1)

#%%
output_file(d + 'windows.html')
p2 = figure(plot_width=1000,
            plot_height=600,
            x_axis_type='datetime',
            title='Window Openings for ' + d.split('/')[-2])
p2.step(df.index[df['opening']=='WindowA'], df['code'][df['opening']=='WindowA'], legend='WindowA', color=colors[0])
p2.step(df.index[df['opening']=='WindowB'], df['code'][df['opening']=='WindowB'], legend='WindowB', color=colors[1])
p2.step(df.index[df['opening']=='WindowC'], df['code'][df['opening']=='WindowC'], legend='WindowC', color=colors[2])
p2.step(df.index[df['opening']=='WindowD'], df['code'][df['opening']=='WindowD'], legend='WindowD', color=colors[3])
p2.step(df.index[df['opening']=='WindowE'], df['code'][df['opening']=='WindowE'], legend='WindowE', color=colors[4])
p2.step(df.index[df['opening']=='WindowF'], df['code'][df['opening']=='WindowF'], legend='WindowF', color=colors[5])
p2.step(df.index[df['opening']=='WindowG'], df['code'][df['opening']=='WindowG'], legend='WindowG', color=colors[6])
#p2.step(df.index[df['opening']=='WindowH'], df['code'][df['opening']=='WindowH'], legend='WindowH', color=colors[7])
#p2.step(df.index[df['opening']=='WindowI'], df['code'][df['opening']=='WindowI'], legend='WindowI', color=colors[8])
show(p2)

#show(column(p1, p2, p3))

#%%
