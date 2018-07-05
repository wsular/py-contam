def readNOAA_ISH(USAF, WBAN, year):
	"""This function reads data from NOAA ISH data files for U.S.
	cities used for CONTAM modeling in the EPA indoor air quality
	project.
	
	Input:
		USAF - USAF station identifier
		WBAN - WBAN station identifier
		year - Desired year, e.g., 2010

	Written by Von P. Walden, Washington State University
	           12 Nov 2017

	"""

	from ish_parser import ish_parser
	import pandas as pd
	import numpy  as np
	
	# Construct filename of the desired data and read entire file.
	fn      = '/Volumes/vonw/data/iaq/NCDC/ish/3505v2' + str(USAF) + '-' + str(WBAN) + str(year) + '.op'
	f       = open(fn)
	content = f.read()
	f.close()
	
	# Read the observations from the desired file.
	wf   = ish_parser()
	wf.loads(content)
	obs  = wf.get_observations()

    # Create a datetime index.
	#
	time = np.array([ob.datetime for ob in obs])

    # ............................... WEATHER DATA ............................
    #
	T    = np.array([ob.air_temperature.get_numeric() for ob in obs])
	P    = np.array([ob.sea_level_pressure.get_numeric() for ob in obs])
	wspd = np.array([ob.wind_speed.get_numeric() for ob in obs])
	wdir = np.array([ob.wind_direction.get_numeric() for ob in obs])
    # Conversion from relative humidity to mixing ration 
    #    ....http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
    A    = 6.116441
    m    = 7.591386
    Tn   = 240.7263
    es   = A*10**(m*(T-273.15)/(T-273.15+Tn))
    ws   = 0.622 * (es/P)
    w    = np.array([ob.humidity.get_numeric() for ob in obs]) * ws * 1000.  # Factor of 1000 converts from kg/kg to g/kg.

	# Create a pandas DataFrame that contains the weather data.
	wth   = pd.DataFrame({'Ta': T,
                          'Pb': P,
                          'Ws': wspd,
                          'Wd': wdir,
                          'Hr': w},
                          index=time)
	
    return wth
