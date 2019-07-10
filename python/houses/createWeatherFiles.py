# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:31:07 2019

@author: Von P. Walden, Washington State University
"""
from contam_input import readHouseData, writeContamWeatherFile

from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column

d   = '/Users/vonw/data/iaq/houses/'

fns = ['H002_summer_weather_final_contam.csv',
       'H002_winter_weather_final_contam.csv',
       'H003_summer_weather_final_contam.csv',
       'H003_winter_weather_final_contam.csv',
       'H004_summer_weather_final_contam.csv',
       'H004_winter_weather_final_contam.csv',
       'H005_summer_weather_final_contam.csv',
       'H006_summer_weather_final_contam.csv',
       'H006_winter_weather_final_contam.csv',
       'H007_summer_weather_final_contam.csv',
       'H007_winter_weather_final_contam.csv',
       'H008_summer_weather_final_contam.csv',
       'H008_winter_weather_final_contam.csv',
       'H009_summer_weather_final_contam.csv',
       'H009_winter_weather_final_contam.csv',
       'H010_summer_weather_final_contam.csv',
       'H010_winter_weather_final_contam.csv']

for fn in fns:
    print('Processing:  ', d + fn)
    
    # Read the weather data and create a dataframe
    wth = readHouseData(d + fn)
    
    # Write the weather data to a contam wth file
    writeContamWeatherFile(d + fn.split('/')[-1][:11] + '.wth', wth)
    
    # Create summary figure
    output_file(d + fn.split('/')[-1][:11] + '.html')
    
    p1 = figure(plot_width=1000,
              plot_height=250,
              x_axis_type='datetime',
              x_axis_label='Time (local)',
              y_axis_label='Pressure (Pa)',
              title=fn.split('/')[-1][:11])
    p1.scatter(wth.index, wth.Pb, color='blue')
    
    p2 = figure(plot_width=1000,
              plot_height=250,
              x_axis_type='datetime',
              x_axis_label='Time (local)',
              y_axis_label='Temperature (K)',
              x_range=p1.x_range)
    p2.scatter(wth.index, wth.Ta, color='red')
    
    p3 = figure(plot_width=1000,
              plot_height=250,
              x_axis_type='datetime',
              x_axis_label='Time (local)',
              y_axis_label='Water Vapor (g/kg)',
              x_range=p1.x_range)
    p3.scatter(wth.index, wth.Hr, color='purple')
    
    p4 = figure(plot_width=1000,
              plot_height=250,
              x_axis_type='datetime',
              x_axis_label='Time (local)',
              y_axis_label='Wind Dir (deg)',
              x_range=p1.x_range)
    p4.scatter(wth.index, wth.Wd, color='lightgreen')
    
    p5 = figure(plot_width=1000,
              plot_height=250,
              x_axis_type='datetime',
              x_axis_label='Time (local)',
              y_axis_label='Wind Spd (m/s)',
              x_range=p1.x_range)
    p5.scatter(wth.index, wth.Ws, color='green')
    
    show(column(p1, p2, p3, p4, p5))
