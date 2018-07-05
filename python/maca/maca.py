class MACA:
    """
    This module reads downscaled climate scenarios from the Northwest Knowledge
    Network at the University of Idaho (http://maca.northwestknowledge.net).
    
    It retrieves data for a given year and location.
    
    Common usage:
        import maca
        maca2006 = maca.MACA(2006,46.7,-117.2)
        data = maca2006.retrieveData()
        plot(data['time'],data['tasmax'])  # plot max temperature for 2006.
        
    Created on Thu Jan 14 14:23:17 2016
    
    @author: Von P. Walden
             Washington State University
    """
        
    def __init__(self, year, lat, lon):
        """Initializes an instance of MACA for a particular year, latitude and longitude.
        
           !!! Currently only works for a single model (BNU-ESM) and scenario (RCP 8.5). !!!"""
        def getMACApixel(maca,lat,lon):
            
            dlat = float(maca.geospatial_lat_resolution)/2.
            dlon = float(maca.geospatial_lon_resolution)/2.
            ilat = np.where((maca.variables['lat'][:] > lat-dlat) & (maca.variables['lat'][:] <= lat+dlat))[0][0]
            ilon = np.where((maca.variables['lon'][:] > lon-dlon) & (maca.variables['lon'][:] <= lon+dlon))[0][0]
            return ilat, ilon
        
        from netCDF4 import Dataset
        from datetime import datetime, timedelta
        import numpy as np
        
        self.year = int(year)
        
        # Define variables and path to MACA file.
        self.directory = 'http://thredds.northwestknowledge.net:8080/thredds/dodsC/agg_macav2metdata_'
        self.scenario  = '_BNU-ESM_r1i1p1_rcp85_2006_2099_CONUS_daily.nc'
        self.files     = ('huss', 
                          'pr', 
                          'rhsmax', 
                          'rhsmin', 
                          'rsds', 
                          'tasmax', 
                          'tasmin', 
                          'uas', 
                          'vas')
        self.variables = ('specific_humidity',
                          'precipitation',
                          'relative_humidity',
                          'relative_humidity',
                          'surface_downwelling_shortwave_flux_in_air',
                          'air_temperature',
                          'air_temperature',
                          'eastward_wind',
                          'northward_wind') 
        # Get index into lat/lon grid for desired location.
        filename       = self.directory + self.files[0] + self.scenario
        data      = Dataset(filename)
        if lon<0:
            lon = 360. + lon
        self.ilat, self.ilon = getMACApixel(data,lat,lon)
        
        # Checks that the desired year is within the temporal limits of the data.
        if ( (year>=2006) & (year<=2099)):
            self.date = np.array([])    
            for d in data.variables['time'][:]:
                self.date = np.append(self.date, datetime(1900,1,1)+timedelta(days=int(d)))
            self.iday = np.where( (self.date>=datetime(year,1,1)) & (self.date<datetime(year+1,1,1)) )
            self.bday = int(self.iday[0][0])
            self.eday = int(self.iday[0][-1])
        else:
            print('ERROR: Desired year is not between 2006 and 2099!!')
        
        data.close()
        
        return
        
    def retrieveData(self):
        """Retrieves MACA data for all variables."""
        
        from netCDF4 import Dataset
        # Now grab the desired year's worth of data.
        d = {}
        for f, v in zip(self.files, self.variables):
            data = Dataset(self.directory + f + self.scenario)
            if f=='huss':  # first variable that is processed; only once.
                d['time'] = data.variables['time'][self.bday:self.eday]
            d[f] = data.variables[v][self.bday:self.eday,self.ilat,self.ilon] 
        
        return d


