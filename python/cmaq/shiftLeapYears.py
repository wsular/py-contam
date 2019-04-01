from glob import glob
from datetime import datetime, timedelta

d     = '/mnt/data/lima/iaq/contam/contaminantFiles/'
dt    = timedelta(days=-1)
years = (1996, 2000, 2004, 2048, 2052, 2088, 2092)

for year in years:
    print('--- ' + str(year))
    fns   = glob(d + str(year) + '*.ctm')
    fns.sort()
    for fn in fns:
        print(fn)
        fi  = open(fn)
        ctm = fi.read()
        fi.close()
        bdate = datetime(year,12,30)
        edate = datetime(year,2,29)
        while(bdate>=edate):
            ctm = ctm.replace(bdate.strftime('%m/%d'), (bdate-dt).strftime('%m/%d'))
            bdate = bdate+dt
        fo = open(d + 'tmp/' + fn.split('/')[-1], 'w')
        fo.write(ctm)
        fo.close
