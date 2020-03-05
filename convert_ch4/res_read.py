import field_read as flr
import orbit_read as orr
import ak_read as akr
from pylab import *
from numpy import *
import time_module as tm
import pres_mod_py as pm
import gp_axis as gax
import obs_operator as obo
import netCDF_gen as nf
import numpy.random as rnd
import oco_units as ounit
import oco_feedback as ofb
import oco_units as ocunit
varnames=['x', 'x0']
resflnm='./std_res/oco_assim_res.2003D008.nc'
x, x0=ofb.ncf_read(resflnm, varnames)

print_x=ocunit.kg_s_to_GtC_Y*x[0:8,0]
print  ' after assimilation', 
print  array2string(print_x, precision=3)

print_x=ocunit.kg_s_to_GtC_Y*x0[0:8,0]
print  ' after assimilation', 
print  array2string(print_x, precision=3)



