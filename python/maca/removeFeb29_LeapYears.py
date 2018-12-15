from glob import glob
import pandas as pd

# For sila
#d = '/Users/vonw/data/maca/'
# For gaia
d = '/mnt/data/lima/iaq/maca'
files = glob(d+'*.csv')

for f in files:
   print(f)
   df = pd.read_csv(f, index_col='time', parse_dates=True)
   dfn = df[~((df.index.month == 2) & (df.index.day == 29))]
   dfn.to_csv(f)
