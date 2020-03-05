#! /geos/u23/python2.5/bin/python2.5
""" the main routin to assimilate OCO observation step by step
"""

# routines to read in GEOS-CHEM outputs ---  not used   
import field_read as flr
# routines to read OCO orbit information --- not used
import orbit_read as orr
# routines to read  BPCH2 files --- not used
import  bpch2_rw_v2 as brw
# routines to generate restart file --- not used  
import restart_tranform as rtf
# routines to generate restart file --- not used  
import ak_read as akr
# pylab for plot --- not used 
from pylab import *
# general numerical calculation routines --- not used
from numpy import *
# routines for time format conversion 
import time_module as tm
# routines to calculate pressure for model levels --- not used 
import pres_mod_py as pm
# class for spatial (or temporal) axes --- not used
import gp_axis as gax 
# oco observation operator  --- not used 
import obs_operator as obo
# routines to write data into netcdf files --- called by the main 
import netCDF_gen as nf
# subroutines to generate random number --- not used 
import numpy.random as rnd
# class for the state vector used in inversion --- not used  
import state_vector_step as stv_c
# general class for Ensemble Kalman filter  --- not used 
import etkf_half as et
# routines for analyzing assimilation feedbackf files --- called by the main 
import oco_feedback as ofb
# routines to collect obs and model values --- not used  
import data_collect_step as dcl
# constants for unit conversions  
import oco_units as ocunit

# basic  routines for r/w netcdf file
from Scientific.IO.NetCDF import *
# class for assimilating OCO observations by Ensemble Kalman Filter.

import oco_assim_step_v2 as ost
# the default settings
import geos_chem_def as gcdf

# create one ost class instance and do initialization 
ocs=ost.oco_assim_step(do_init_run=True)

for i in range(0, gcdf.ntime_geos_chem):
    
    sstep=r'%2.2d' % (i)
    resflnm=gcdf.inv_path+"oco_assim_res"+"."+ocs.select_mode+"_"+sstep+".nc"
    # ocs.do_one_step(update_step=0, rerun_step=0, do_read_mean_step=0)
    ocs.do_one_assimilation(update_step=0)
    
    
    xne=arange(ocs.ne)
    xnx=arange(ocs.nx)
    ne0=size(ocs.dx0[0,:])
    xne0=arange(ne0)
    nst=ocs.cur_step
    xstep=arange(ocs.cur_step)
    dimnames=['nx', 'ne', 'ne0', 'nst']
    dimvars=[xnx, xne, xne0, xstep]
    dimtypes=['i', 'i','i', 'i']
    
    print ocs.ne, ocs.nx, ocs.cur_step
    
    print shape(ocs.xtm)
    print shape(ocs.dx)
    
    # out put to the restart file
    
    xtm_info=ofb.geos_varinfo('sum_xtm', 'f', ['ne', 'ne'], ocs.xtm)
    x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    x0_info=ofb.geos_varinfo('x0', 'f', ['nx'], ocs.mean_x0)
    dx_info=ofb.geos_varinfo('dx', 'f', ['nx', 'ne'], ocs.dx)
    dx0_info=ofb.geos_varinfo('dx0', 'f', ['nx', 'ne0'], ocs.dx0)
    doy_info=ofb.geos_varinfo('doy', 'i', ['nst'], ocs.co2.doy[0:nst])
    yyyy_info=ofb.geos_varinfo('yyyy', 'i', ['nst'], ocs.co2.yyyy[0:nst])  # year for emission period

    # x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    # ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, [x_info, dx_info, xtm_info])
    
    ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, [dx_info, \
                                                                    dx0_info, xtm_info, \
                                                                    x_info, x0_info, \
                                                                    yyyy_info, doy_info])
    
    ocs.re_select_ensemble()
    if (i>-1):
        do_run=True
    else:
        do_run=False
    ocs.rerun_geos_chem(resflnm='xrestart',  do_run=do_run)
   
        
    

                                                                
