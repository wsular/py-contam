# -*- coding: utf-8 -*-
"""
Created on Thu May 19 21:14:35 2016

@author: Von P. Walden, Washington State University
"""
import pandas as pd
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, show, vplot
from bokeh.plotting import figure

##############################################################################
# Input/Output
##############################################################################
# .... Read in summary Excel file for house.
fn = '/Users/vonw/work/projects/iaq/data/home2/combined-home2-winter-data.xlsx'
house       = pd.read_excel(fn, header=[0], skiprows=[1])
house.index = house.timestamp
# .... Resample data to 5-minute averages to reduce the size of the html file.
house       = house.resample('5min').mean()

# .... Set output filename.
output_file('/Users/vonw/data/iaq/house2_winter.html')

##############################################################################
# Plotting
##############################################################################
# ....Dust
p1 = figure(plot_width=1000, 
            plot_height=600, 
            x_axis_type='datetime', 
            x_axis_label='Time (local)',
            y_axis_label='Concentration (mg m-3)',
            title='Indoor and Outdoor Dust',
            tools=['pan','box_zoom','save','reset'])
p1.line(house.index, house.outdoor_dusttrak2_pm25,color='navy', legend='outdoor', line_width=2)
p1.line(house.index, house.inside_dusttrak2_pm25 ,color='red' , legend='indoor',  line_width=2)
pm2_5 = Panel(child=p1, title='PM2.5')

# ....CO2
p2 = figure(plot_width=1000, 
            plot_height=600, 
            x_axis_type='datetime', 
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppmv)',
            title='Indoor and Outdoor Carbon Dioxide',
            tools=['pan','box_zoom','save','reset'])
p2.line(house.index, house.outdoor_li840a_CO2,color='navy', legend='outdoor', line_width=2)
p2.line(house.index, house.inside_li840a_CO2, color='red' , legend='indoor',  line_width=2)
CO2  = Panel(child=p2, title="CO2")

# ....H2O
p3 = figure(plot_width=1000, 
            plot_height=600, 
            x_axis_type='datetime', 
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppthv))',
            title='Indoor and Outdoor Water Vapor',
            tools=['pan','box_zoom','save','reset'])
p3.line(house.index, house.outdoor_li840a_H2O,color='navy', legend='outdoor', line_width=2)
p3.line(house.index, house.inside_li840a_H2O, color='red' , legend='indoor',  line_width=2)
H2O  = Panel(child=p3, title="H2O")

# ....O3
p4 = figure(plot_width=1000, 
            plot_height=600, 
            x_axis_type='datetime', 
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppbv)',
            title='Indoor and Outdoor Ozone',
            tools=['pan','box_zoom','save','reset'])
p4.line(house.index, house.outdoor_m205_O3,color='navy', legend='outdoor', line_width=2)
p4.line(house.index, house.indoor_m205_O3, color='red' , legend='indoor',  line_width=2)
O3   = Panel(child=p4, title="O3")

# ....NOx
p5a = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppbv)',
            title='Indoor and Outdoor NO2',
            tools=['pan','box_zoom','save','reset'])
p5a.line(house.index, house.outdoor_m42C_NO2,color='navy', legend='outdoor', line_width=2)
p5a.line(house.index, house.indoor_m42C_NO2, color='red' , legend='indoor',  line_width=2)
p5b = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_range=p5a.x_range,
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppbv)',
            title='Indoor and Outdoor NO',
            tools=['pan','box_zoom','save','reset'])
p5b.line(house.index, house.outdoor_m42C_NO,color='navy', legend='outdoor', line_width=2)
p5b.line(house.index, house.indoor_m42C_NO, color='red' , legend='indoor',  line_width=2)
p5c = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_range=p5a.x_range,
            x_axis_label='Time (local)',
            y_axis_label='Concentration (ppbv)',
            title='Indoor and Outdoor NOx',
            tools=['pan','box_zoom','save','reset'])
p5c.line(house.index, house.outdoor_m42C_NOx,color='navy', legend='outdoor', line_width=2)
p5c.line(house.index, house.indoor_m42C_NOx, color='red' , legend='indoor',  line_width=2)
p5   = vplot(p5a,p5b,p5c)
NOx  = Panel(child=p5, title="NOx")

# ....Met
p6a = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            title='Airmar200 Weather Data',
            x_axis_label='Time (local)',
            y_axis_label='Pressure (mb)',
            tools=['pan','box_zoom','save','reset'])
p6a.line(house.index, house.airmar200wx_P_baro, color='navy', line_width=2)
p6b = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_range=p6a.x_range,
            x_axis_label='Time (local)',
            y_axis_label='Temperature (C)', 
            tools=['pan','box_zoom','save','reset'])
p6b.line(house.index, house.airmar200wx_T_air, color='red', legend='T', line_width=2)
p6b.line(house.index, house.airmar200wx_dewpoint, color='navy', legend='Td', line_width=2)
p6c = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_range=p6a.x_range,
            x_axis_label='Time (local)',
            y_axis_label='Speed (m/s)', 
            tools=['pan','box_zoom','save','reset'])
p6c.line(house.index, house.airmar200wx_WS, color='navy', line_width=2)
p6d = figure(plot_width=1000, 
            plot_height=300, 
            x_axis_type='datetime', 
            x_range=p6a.x_range,
            x_axis_label='Time (local)',
            y_axis_label='Direction (degTN)',
            tools=['pan','box_zoom','save','reset'])
p6d.line(house.index, house.airmar200wx_WD_true, color='navy', line_width=2)
p6   = vplot(p6a,p6b,p6c,p6d)
met  = Panel(child=p6, title="Meteorology")

# .... Combine plots and show html file
tabs = Tabs(tabs=[ pm2_5, CO2, H2O, O3, NOx, met ])
show(tabs)