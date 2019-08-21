#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 19:22:52 2019

@author:    Von P. Walden
            Washington State University
"""
import pandas as pd
import contam_input as contam
from bokeh.plotting import figure, output_file, show
from bokeh.layouts import column

# ....Read weather data
wth = pd.read_csv('/Users/vonw/data/iaq/houses/weatherFiles/H005_summer.wth', 
                  sep='\t', 
                  skiprows=18, 
                  header=None, 
                  names=['date', 'time', 'Ta', 'Pb', 'Ws', 'Wd', 'Hr', 'Ith', 'Idn', 'Ts', 'Rn', 'Sn'])
dates           = wth['date'].str.split('/', expand=True)
times           = wth['time'].str.split(':', expand=True)
wth['year']     = 2016
wth['month']    = dates[0]
wth['day']      = dates[1]
wth['hour']     = times[0]
wth['minute']   = times[1]
wth['second']   = times[2]
wth.index       = pd.to_datetime(wth[['year', 'month', 'day', 'hour', 'minute', 'second']])

# ....Read contaminant data
ds  = ['/Users/vonw/data/iaq/houses/outdoors/h005_outdoor_summer/']
d  = ds[0]
ctm, units = contam.readHouseContaminantData(d)

# ....Create Bokeh html plot
output_file(d+'h005.html')

p1 = figure(plot_width=1000,
           plot_height=250,
           x_axis_type='datetime',
           y_axis_label='Temperature (K)',
           title=d.split('/')[-2])
p1.line(wth.index, wth.Ta.values)

p2 = figure(plot_width=1000,
           plot_height=250,
           x_axis_type='datetime',
           x_range=p1.x_range,
           y_axis_label='Ozone (ppb)',
           title=None)
p2.line(ctm.loc['rack'].index, ctm.loc['rack']['O3'].values)

p3 = figure(plot_width=1000,
           plot_height=250,
           x_axis_type='datetime',
           x_range=p1.x_range,
           y_axis_label='PM2.5 (ug m-3)',
           title=None)
p3.line(ctm.loc['pm25'].index, ctm.loc['pm25']['PM2.5'].values)

p4 = figure(plot_width=1000,
           plot_height=250,
           x_axis_type='datetime',
           x_range=p1.x_range,
           y_axis_label='HCHO (ppb)',
           title=None)
p4.line(ctm.loc['ptrms'].index, ctm.loc['ptrms']['Formaldehyde'].values)

show(column(p1, p2, p3, p4))