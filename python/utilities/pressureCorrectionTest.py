#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:26:26 2017

@author: Von P. Walden, Washington State University
"""
# Script to check if the calculation to convert sea level pressure to station
#   pressure is accurate. The calculation comes from 
#   https://www.weather.gov/media/epz/wxcalc/stationPressure.pdf.
#   This was compared to a calculation using the Hypsometric equation.

import numpy as np
import matplotlib.pyplot as plt

def estimate1(hm, Ts):
    return ((Ts - (0.0065*hm))/Ts)**5.2561

def estimate2(hm, Ts):
    Tave = (Ts + (Ts-0.0065*hm))/2
    H    = 287 * Tave / 9.8
    return np.exp(-hm/H)

# Height scale in meters (from 0 to 6000 feet)
hm = np.arange(0,6000,50)*0.3048

# Figure showing comparisons of different estimates for three temperatures.
plt.figure()
plt.subplot(311)
plt.xticks([])
plt.plot(hm, estimate1(hm,250),'o', hm, estimate2(hm,250),'.')
plt.title('Ts = 250 K')
plt.subplot(312)
plt.plot(hm, estimate1(hm,288),'o', hm, estimate2(hm,288),'.')
plt.xticks([])
plt.ylabel('P multiplications factor')
plt.title('Ts = 288 K')
plt.subplot(313)
plt.plot(hm, estimate1(hm,310),'o', hm, estimate2(hm,310),'.')
plt.xlabel('Height, meters')
plt.title('Ts = 310 K')

plt.savefig('/Users/vonw/work/software/iaq/2015-iaq-contam-input/python/pressureCorrectionTest.png')
