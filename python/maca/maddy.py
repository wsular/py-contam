
##############################################################################

# Import the maca function from the python file.
from maca_aeolus import maca

# Set up all the variables you want.
fvar = 'tasmax'
rcp = 4.5
models = ['BNU-ESM']
beginningDate = '1950-1-1'
endingDate = '2007-1-1'
latitude = 46.7
longitude = 242.8
data1 = maca(fvar,models,rcp,beginningDate,endingDate,latitude,longitude)

# Now try access multiple models at once.
models = ['BNU-ESM', 'NorESM1-M', 'CCSM4']
data2 = maca(fvar,models,rcp,beginningDate,endingDate,latitude,longitude)

# Save both the pandas DataFrames.
data1.to_csv('data1.dat')
data2.to_csv('data2.dat')

##############################################################################

# Transfer data files, data1.dat and data2.dat, back to laptop.
# Start ipython on laptop and type: %pylab

# Read the data back into python.
import pandas as pd
data1 = pd.read_csv('data1.dat', header=0, index_col='time', parse_dates=True)
data2 = pd.read_csv('data2.dat', header=0, index_col='time', parse_dates=True)

# Create plots.

# type this in ipython first: %pylab
# ....plot single model
figure()
plot(data1.index, data1['BNU-ESM'])
# ....plot for multiple models.
figure()
plot(data2.index, data2['BNU-ESM'], data2.index, data2['NorESM1-M'])
# ....or using the DataFrame
figure()
data2.plot()   # Takes a bit longer...

# Statistics of DataFrame columns (models)
# ....for a single model
data1.describe()
# ....or
data1['BNU-ESM'].describe()
# ....for multiple models
data2.describe()

##############################################################################
