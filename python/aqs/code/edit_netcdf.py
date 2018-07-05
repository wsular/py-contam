# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 12:44:20 2017

@author: lar
"""

from netCDF4 import Dataset

fn  = '/fastscratch/airpact5/rerun/TCOPS/2016/2016072500/EMISSION/merged/test/EMISSIONS_3D_AIRPACT_04km_20160725.ncf'
emis = Dataset(fn,'r')
ALD2 = emis.variables['ALD2'][:]*1.3
ALDX = emis.variables['ALDX'][:]*1.3
ETHA = emis.variables['ETHA'][:]*1.3
ETOH = emis.variables['ETOH'][:]*1.3
ETH = emis.variables['ETH'][:]*1.3
FORM = emis.variables['FORM'][:]*1.3
IOLE = emis.variables['IOLE'][:]*1.3
ISOP = emis.variables['ISOP'][:]*1.3
MEOH = emis.variables['MEOH'][:]*1.3
OLE = emis.variables['OLE'][:]*1.3
PAR = emis.variables['PAR'][:]*1.3
SESQ = emis.variables['SESQ'][:]*1.3
TERP = emis.variables['TERP'][:]*1.3
TOL = emis.variables['TOL'][:]*1.3
XYL = emis.variables['XYL'][:]*1.3
emis.close()
