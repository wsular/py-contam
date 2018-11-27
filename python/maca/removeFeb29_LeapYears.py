from glob import glob
import pandas as pd

d = '/Users/vonw/data/maca/'
files = glob(d+'*.csv')

for f in files:
   df = pd.read_csv(f, index_col='time', parse_dates=True)
   dfn = df[~((df.index.month == 2) & (df.index.day == 29))]
   dfn.to_csv(f)
