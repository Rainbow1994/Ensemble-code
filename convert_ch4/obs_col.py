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

        

yyyy=2003
doy0=1
doy1=96 # 096 0406
doys=arange(doy0, doy1)
iday=0
nusd_obs=0
fclim=open('clim_co2.dat', 'r')
lines=fclim.readlines()
fclim.close()
aprior=list()
apr_pres=list()
for iline in lines:
    terms=iline.split()
    aprior.append(float(terms[1]))
    apr_pres.append(float(terms[0]))

aprior=array(aprior)
apr_pres=array(apr_pres)
apr_pres=log10(apr_pres)


for doy in doys:
    yyyy, mm,dd=tm.doy_to_time_array(doy, yyyy)
    print 'year mm dd', yyyy, mm, dd
    obs=obo.obs_operator(yyyy, mm, dd, 1, 185, \
                         aprior=aprior, apr_pres=apr_pres)
    sdate=r'%4.4dD%3.3d' % (yyyy, doy)
    ncflnm="oco"+"."+sdate+".nc"
    
    for ii in range(1,185):
        if (ii==1):
            obs.get_obs_prof(ii)
        else:
            obs.get_obs_prof(ii, do_update=False)
        xgp=obs.obs_xgp[ii-1]
        print shape(xgp)
    
    obs_err=obs.obs_err
    obs_err=array(obs_err)
    print 'shape obs+err', shape(obs_err)
    rnd_obs_err=array(obs_err)
    for iobs  in range(size(obs_err)):
        err_val=obs_err[iobs]
        
        rnd_err=rnd.normal(scale=err_val)
        rnd_obs_err[iobs]=rnd_err
    
                           
    cflag=obs.obs_cflag
    otime=obs.obs_time
    olat=obs.obs_lat
    olon=obs.obs_lon

    dimTypes=['f']
    dimVars=[otime]    
    dimNames=['time']
    # nf.netCDF_def_dims(ncflnm,dimNames,dimTypes, dimVars)

    # lon
    
    varName='lon'
    varType='f'
     
    varData=olon

    # nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)
    
    # lat
    
    varName='lat'
    varType='f'
     
    varData=olat

    # nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)

    # cflag
    
    varName='cloud'
    varType='i'
     
    varData=cflag

    # nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)

    # xco2
    
    varName='xco2'
    varType='f'

    print shape(xgp), shape(rnd_obs_err)
    rnd_obs_err=1.0e-6*rnd_obs_err
    varData=xgp+rnd_obs_err
    

    # nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)
    
    varName='err'
    varType='f'
     
    varData=1.0e-6*obs_err
    
    # nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)
    
