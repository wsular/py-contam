# Read netCDF file into an xarray dataset.
import xarray as xr
h002_summer = xr.open_dataset('/home/lima/data/iaq/test_homes_modeling/no_opening/h002_summer.nc')

# Display the contents of the house file
h002_summer

# Display a single variable in the house file
h002_summer.outsideAirTemperature

# Display the data (as a numpy array) a single variable in the house file
h002_summer.outsideAirTemperature.values

# Display the attributes of a single variable in the house file
h002_summer.outsideAirTemperature.attrs

# Plot the data of this variable using bokeh
from bokeh.plotting import figure, output_file, show

output_file('h002_summer-outsideAirTemperature.html')

p = figure(plot_width=1000,
           plot_height=600,
           x_axis_type='datetime')
p.line(h002_summer.time.values, h002_summer.outsideAirTemperature.values)
show(p)
