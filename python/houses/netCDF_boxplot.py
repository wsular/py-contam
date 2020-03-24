import pandas as pd
import xarray as xr
from glob import glob

# ....Read in the data from multiple houses
d = '/Users/vonw/data/iaq/test_homes_modeling/no_opening/'
files = glob(d+'*.nc')
files.sort()
houses = [file.split('.')[0].split('/')[-1]  for file in files]

oat = pd.DataFrame({})
for house, file in zip(houses, files):
    ds = xr.open_dataset(file)
    oat = pd.concat([oat,ds.outsideAirTemperature.to_dataframe()], ignore_index=True, axis=1)

oat.columns = houses

# Create a boxplot using matplotlib
import matplotlib.pyplot as plt
plt.figure()
oat.boxplot()
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
