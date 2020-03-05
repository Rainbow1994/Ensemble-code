from pylab import *
from numpy import *
from Scientific.IO.NetCDF import *
ncf=NetCDFFile("oco_glint.2003D003.nc")
print ncf.variables.keys()
co2=ncf.variables['xco2']
co2=array(co2)
co2=squeeze(co2)
err=ncf.variables['err']
err=array(err)
err=squeeze(err)

ix=arange(0, 20)
errorbar(ix, co2[0:20], err[0:20])
show()


    
