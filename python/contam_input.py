# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:41:45 2017

@author: Von P. Walden, Washington State University
"""

def readWRF_CMAQ(gridFile, dataFile, lat, lon):
    """
    This function reads data from a WRF CMAQ data file into a pandas dataframe, df.
    The dataframe can then be written to a CONTAM weather file using function,
    writeContamWeatherFile.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    2 Jun 2017
    """
    import xarray as xr
    import numpy  as np
    import pandas as pd
    from   datetime import datetime, timedelta
    
    def find_WRF_pixel(latvar,lonvar,lat0,lon0):
        # Read latitude and longitude from file into numpy arrays
        # Renamed findWRFpixel from original function, naive_fast, written by Vikram Ravi.
        latvals = latvar[:]
        lonvals = lonvar[:]
        dist_sq = (latvals-lat0)**2 + (lonvals-lon0)**2
        minindex_flattened = dist_sq.argmin()  # 1D index of min element
        iy_min,ix_min = np.unravel_index(minindex_flattened, latvals.shape)
        return int(iy_min),int(ix_min)
        
    # Open the WRF GRIDCRO2D file to determine the WRF pixel for lat/lon.
    GRID = xr.open_dataset(gridFile)
    ilat, ilon = find_WRF_pixel(GRID.LAT[0,0,:,:].values,GRID.LON[0,0,:,:].values,lat,lon)
    
    # Open WRF-CMAQ data file.
    DATA = xr.open_dataset(dataFile)
    # Create a datetime index.
    datestr = str(DATA.SDATE)
    date    = datetime(int(datestr[0:4]),1,1) + timedelta(int(datestr[4:])-1)
    time    = [date + timedelta(hours=float(t)) for t in DATA.TSTEP]
    #
    # ............................... WEATHER DATA ............................
    #
    # Read meteorological data from WRF-CMAQ data file.
    T    = DATA.SFC_TMP.values[:,0,ilat,ilon] + 273.15   # in K
    P    = DATA.AIR_DENS.values[:,0,ilat,ilon]*287.0*T
    wspd = DATA.WSPD10.values[:,0,ilat,ilon]
    wdir = DATA.WDIR10.values[:,0,ilat,ilon]
    # Conversion from relative humidity to mixing ration 
    #    ....http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
    A    = 6.116441
    m    = 7.591386
    Tn   = 240.7263
    es   = A*10**(m*(T-273.15)/(T-273.15+Tn))
    ws   = 0.622 * (es/P)
    w    = DATA.RH.values[:,0,ilat,ilon] * ws * 1000.  # Factor of 1000 converts from kg/kg to g/kg.
    
    # Create a pandas dataframe with meteorological variables.
    wth   = pd.DataFrame({'Ta':T, 
                          'Pb':P,
                          'Ws':wspd,
                          'Wd':wdir,
                          'Hr':w},
                          index=time)
    #
    # ........................... CONTAMINANT DATA ............................
    #
    # Read contaminat data from WRF-CMAQ data file.

    return wth

def readNOAA_ISH(USAF, WBAN, year):
    """This function reads data from NOAA ISH data files for U.S.
    cities used for CONTAM modeling in the EPA indoor air quality
    project.
    
    Input:
        USAF - USAF station identifier  (as a string)
        WBAN - WBAN station identifier  (as a string)
        year - Desired year, e.g., 2010 (as an integer)

    Written by Von P. Walden, Washington State University
               12 Nov 2017

    """
    """
    isd-history-IAQ.csv
        "CITY","USAF","WBAN","STATION NAME","CTRY","STATE","ICAO","LAT","LON","ELEV(M)","BEGIN","END"
        "Chicago","725300","94846","CHICAGO O'HARE INTERNATIONAL AIRPORT","US","IL","KORD","+41.995","-087.934","+0201.8","19461001","20171107"
        "Cincinnati","724210","93814","CINCINNATI/NORTHERN KENTUCKY INTL AP","US","KY","KCVG","+39.044","-084.672","+0269.1","19730101","20171107"
        "Nashville","723270","13897","NASHVILLE INTERNATIONAL AIRPORT","US","TN","KBNA","+36.119","-086.689","+0182.9","19510101","20171108"
        "Birmingham","722280","13876","BIRMINGHAM INTERNATIONAL AIRPORT","US","AL","KBHM","+33.566","-086.745","+0187.5","19420801","20171107"
        "NewYork","725030","14732","LA GUARDIA AIRPORT","US","NY","KLGA","+40.779","-073.880","+0003.4","19730101","20171107"
        "Buffalo","725280","14733","BUFFALO NIAGARA INTERNATIONAL AP","US","NY","KBUF","+42.941","-078.736","+0218.2","19420201","20171107"
        "Phoenix","722780","23183","PHOENIX SKY HARBOR INTL AIRPORT","US","AZ","KPHX","+33.428","-112.004","+0337.4","19730101","20171107"
        "Denver","725650","03017","DENVER INTERNATIONAL AIRPORT","US","CO","KDEN","+39.833","-104.658","+1650.2","19940718","20171107"
        "Boston","725090","14739","GEN E L LOGAN INTERNATIONAL AIRPORT","US","MA","KBOS","+42.361","-071.010","+0003.7","19431121","20171107"
        "Worcester","725100","94746","WORCESTER REGIONAL AIRPORT","US","MA","KORH","+42.271","-071.873","+0304.8","20100801","20171107"
        "LosAngeles","722950","23174","LOS ANGELES INTERNATIONAL AIRPORT","US","CA","KLAX","+33.938","-118.389","+0029.6","19440101","20171107"
        "Seattle","727930","24233","SEATTLE-TACOMA INTERNATIONAL AIRPORT","US","WA","KSEA","+47.444","-122.314","+0112.8","19480101","20171107"
        "Miami","722020","12839","MIAMI INTERNATIONAL AIRPORT","US","FL","KMIA","+25.791","-080.316","+0008.8","19730101","20171107"
        "WashingtonDC","724030","93738","WASHINGTON DULLES INTERNATIONAL AP","US","VA","KIAD","+38.935","-077.447","+0088.4","19730101","20171107"
        "Atlanta","722190","13874","HARTSFIELD-JACKSON ATLANTA INTL AP","US","GA","KATL","+33.630","-084.442","+0307.9","19730101","20171108"
        "Minneapolis","726580","14922","MINNEAPOLIS-ST PAUL INTERNATIONAL AP","US","MN","KMSP","+44.883","-093.229","+0265.8","19450101","20171107"
        "StLouis","724340","13994","LAMBERT-ST LOUIS INTERNATIONAL AP","US","MO","KSTL","+38.753","-090.374","+0161.9","19730101","20171107"
        "Dallas","722590","03927","DALLAS/FT WORTH INTERNATIONAL AP","US","TX","KDFW","+32.898","-097.019","+0170.7","19730101","20171107"
        "CorpusChristi","722510","12924","CORPUS CHRISTI  INTERNATIONAL AIRPORT","US","TX","KCRP","+27.774","-097.512","+0013.4","19460801","20171107"
    """

    def pressureCorrection(Ps, Hstn, Tstn):
        """Calculate the station pressure in hPa from the sea-level pressure
        (Ps) and the station temperature (Tstn). The correction comes from
        http://www.weather.gov/media/epz/wxcalc/stationPressure.pdf. This
        correction was quickly checked against the hypsometric equation and was
        shown to be adequate; see pressureCorrectionTest.py.
        
        Inputs:
            Hstn - elevation (height) of weather station (meters)
            Ps   - sea-level pressure in Pa
            Tstn - temperature measured at the weather station (K)
        
        Output:
            Atmospheric pressure at the weather station
            
        Written by Von P. Walden, Washington State University
                    19 November 2017
        """
        Lrate = 0.0065*Hstn     # LRate is the approximate lapse rate (K m-1)
        return Ps*((Tstn - Lrate)/Tstn)**5.2561
    
    # NOAA ISH parser comes from:
    #    https://github.com/haydenth/ish_parser
    from ish_parser import ish_parser
    import pandas as pd
    import numpy  as np
    
    # Construct filename of the desired data and read entire file.
    fn      = '/Volumes/vonw/data/iaq/NCDC/ish/3505v2' + USAF + '-' + WBAN + str(year) + '.op'
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
    Hstn = np.array([ob.elevation for ob in obs])                               # meters
    T    = np.array([ob.air_temperature.get_numeric() for ob in obs])           # deg C
    Ps   = np.array([ob.sea_level_pressure.get_numeric() for ob in obs])*100.   # Pa
    Pb   = pressureCorrection(Ps, Hstn, T+273.15)                               # Pa
    wspd = np.array([ob.wind_speed.get_numeric() for ob in obs])                # m s-1 
    wdir = np.array([ob.wind_direction.get_numeric() for ob in obs])            # degrees
    # Conversion from relative humidity to mixing ration 
    #    ....http://www.vaisala.com/Vaisala%20Documents/Application%20notes/Humidity_Conversion_Formulas_B210973EN-F.pdf
    A    = 6.116441
    m    = 7.591386
    Tn   = 240.7263
    es   = A*10**(m*(T)/(T+Tn))
    ws   = 0.622 * (es/Pb)
    w    = np.array([ob.humidity.get_numeric() for ob in obs]) * ws * 1000.     # Factor of 1000 converts from kg/kg to g/kg.
    # Calculation of air density
    Rd   = 287.                                                                 # Gas constant for dry air; J kg-1 K-1
    rho  = Pb / (Rd * (T+273.15))
    # Create a pandas DataFrame that contains the weather data.
    wth   = pd.DataFrame({'Ta'       : T+273.15,
                          'Pb'       : Pb,
                          'Ws'       : wspd,
                          'Wd'       : wdir,
                          'Hr'       : w,
                          'rho'      : rho,
                          'elevation': Hstn},
                          index=time)
    
    # Resample the dataframe to an hourly time step.
    wth = wth.resample('H').mean()
    
    return wth

def readMACA(city, year, rcp, model):
    """
    This function reads data from a data file of MACA downscaled climate data 
    into a pandas dataframe, df. The dataframe can then be written to a CONTAM 
    weather file using function, writeContamWeatherFile. It assumes the user
    wants to generate data files for ALL of the 19 contam cities.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    4 Oct 2017
    """
    import pandas as pd
    import numpy  as np
    import pytz
    import ephem
    import sys
    from socket import gethostname
    
    def solar_times(city, date):
        # Sets up the Observer using the city's lat/lon.
        tz      = pytz.timezone(city.time_zone)
        o       = ephem.Observer()
        o.date  = (date + pd.Timedelta('9 hours')).astimezone(pytz.UTC)
        o.lat   = city.latitude*np.pi/180.
        o.long  = (360.+city.longitude)*np.pi/180.
        o.elev  = city.altitude
        sun     = ephem.Sun()
        sunrise = o.previous_rising(sun)
        noon    = o.next_transit(sun, start=sunrise)
        sunset  = o.next_setting(sun, start=noon)
        # Convert from UTC to local time zone.
        local_sunrise = pytz.utc.localize(sunrise.datetime(), is_dst=None).astimezone(tz)
        local_noon    = pytz.utc.localize(noon.datetime(),    is_dst=None).astimezone(tz)
        local_sunset  = pytz.utc.localize(sunset.datetime(),  is_dst=None).astimezone(tz)
        return local_sunrise, local_noon, local_sunset
    
    # Read in data files depending on year and RCP.
    hostname = gethostname()
    if hostname.find('petb227a') >= 0:    # This is the hostname for gaia.
        directory = '/mnt/data/lima/iaq/maca/'
    elif hostname.find('sila') >= 0:
        directory = '/Volumes/vonw/data/iaq/maca/'
    else:
        print('Not a valid computer for access to MACA data. Try again...')
        sys.exit()
    if ((year>=1996) and (year<=2006)):
        yearstr = '_1995_2006.csv'
    elif ((year>=2010) and (year<=2020)):
        yearstr = '_2009_2020.csv'
    elif ((year>=2030) and (year<=2040)):
        yearstr = '_2029_2040.csv'
    elif ((year>=2044) and (year<=2056)):
        yearstr = '_2044_2056.csv'
    elif ((year>=2086) and (year<=2095)):
        yearstr = '_2085_2096.csv'
    elif ((year>=2096) and (year<=2098)):
        yearstr = '_2089_2099.csv'
    else:
        print('Incorrect year. Try again...')
        return
    
    # Create dataframes from desired data files.
    tasmax = pd.read_csv(directory + city.city + '_tasmax_' + str(rcp) + yearstr, index_col='time', parse_dates=True)
    tasmin = pd.read_csv(directory + city.city + '_tasmin_' + str(rcp) + yearstr, index_col='time', parse_dates=True)
    huss   = pd.read_csv(directory + city.city + '_huss_'   + str(rcp) + yearstr, index_col='time', parse_dates=True)
    pr     = pd.read_csv(directory + city.city + '_pr_'     + str(rcp) + yearstr, index_col='time', parse_dates=True)
    uas    = pd.read_csv(directory + city.city + '_uas_'    + str(rcp) + yearstr, index_col='time', parse_dates=True)
    vas    = pd.read_csv(directory + city.city + '_vas_'    + str(rcp) + yearstr, index_col='time', parse_dates=True)
    
    # Create DAILY time series for the desired year and model.
    b      = str(year)+'-01-01'
    e      = str(year+1)+'-01-01'   
    Ps     = 101325. * (1 - 2.25577e-5 * city.altitude)**5.25588      # Very simple conversion from altitude to pressure; https://www.engineeringtoolbox.com/air-altitude-pressure-d_462.html
    Tmax   = tasmax[b:e][model]
    Tmin   = tasmin[b:e][model]
    Tavg   = pd.concat((Tmax,Tmin),axis=1).mean(axis=1)
    Hr     = huss[b:e][model] / (1 - huss[b:e][model]) * 1000.  # convert from specific humidity to mixing ratio, then from kg kg-1 to g kg-1.
    prcp   = pr[b:e][model]
    wspd   = (uas[b:e][model]**2 + vas[b:e][model]**2)**0.5
    wdir   = np.arctan2(uas[b:e][model],vas[b:e][model])
    wdir[wdir>=0.] = wdir[wdir>=0.]*180/np.pi
    wdir[wdir<0.]  = 360. + (wdir[wdir<0.]*180/np.pi)
    daily  = pd.DataFrame({'Ps':   Ps,
                           'Tmax': Tmax,
                           'Tmin': Tmin,
                           'prcp': prcp,
                           'wspd': wspd,
                           'wdir': wdir,
                           'Hr':   Hr},
                           index=Tmax.index).tz_localize(city.time_zone)
        
    # Creates a weather dataframe with an HOURLY timescale; winds and RH are interpolated.
    time  = pd.date_range(str(year)+'-01-01',str(year)+'-12-31 23',freq='H',tz=city.time_zone)
    wth   = pd.DataFrame({'Pb':daily.Ps.resample('H').ffill(),
                          'Ws':daily.wspd.resample('H').interpolate(),
                          'Wd':daily.wdir.resample('H').interpolate(),
                          'Hr':daily.Hr.resample('H').interpolate()},
                          index=time)
    
    # Generate time series of daily max and min temperatures (for interpolation).
    t = []
    T = []
    for day in daily.itertuples():
        sunrise, noon, sunset = solar_times(city, day.Index.to_pydatetime())
        t.append(sunrise)
        T.append(day.Tmin)
        t.append(noon+pd.Timedelta('3 hours'))   # This is a guess as to when Tmax occurs.
        T.append(day.Tmax)

    x  = np.array([time.timestamp() for time in wth.index])
    xp = np.array([time.timestamp() for time in t])
    fp = np.array(T)
    Ta = np.interp(x,xp,fp,fp[0],fp[-1])
    wth['Ta'] = Ta
    
    return wth

def writeContamWeatherFile(wthrFile, df):
    """
    This function writes the data in the pandas dataframe, df, to a text file.
    The text file is formatted as a CONTAM weather file.
    
        Written by  Von P. Walden
                    Washington State University
                    Laboratory for Atmospheric Research
                    2 Jun 2017
    """
    # Open new weather file.
    fp = open(wthrFile, 'w')
    
    # Write the first header lines.
    fp.write('WeatherFile ContamW 2.0\n\n');
    fp.write(df.index[0].to_pydatetime().strftime('%m/%d')  + '	 !start-of-file date\n');
    fp.write(df.index[-1].to_pydatetime().strftime('%m/%d') + '	 !end-of-file date\n');
    fp.write('!Date	DofW	Dtype	DST	Tgrnd [K]\n');
    
    # Write daily average data.
    dfa = df.resample('1D').mean()
    for day in dfa.index:
        fp.write(  day.strftime('%m/%d') + '\t' 
                 + str(day.weekday()+1)     + '\t'
                 + str(day.weekday()+1)     + '\t{0:2d}\t{1:10.2f}\n'.format(day.timetuple().tm_isdst,dfa.loc[day]['Ta']))
            
    # Write the second header line.
    fp.write('!Date	Time	Ta [K]	Pb [Pa]	Ws [m/s]	Wd [deg]	Hr [g/kg]	Ith [kJ/m^2]	Idn [kJ/m^2]	Ts [K]	Rn [-]	Sn [-]\n');

    # Write the hourly data.
    for hour in df.index:
        fp.write(  hour.strftime('%m/%d') + '\t'
                 + hour.strftime('%H:%M:%S') 
                 + '\t{0:10.2f}\t{1:10.2f}\t{2:10.2f}\t{3:10.2f}\t{4:10.2f}\t{5:10.2f}\t{6:10.2f}\t{7:10.2f}\t{8:10.2f}\t{9:10.2f}\n'.format(df.loc[hour]['Ta'],df.loc[hour]['Pb'],df.loc[hour]['Ws'],df.loc[hour]['Wd'],df.loc[hour]['Hr'],0.,0.,0.,0.,0.))
    
    # Close the weather file.
    fp.close()
    
    return
