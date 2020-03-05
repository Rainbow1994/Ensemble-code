#! /home/lfeng/tmp_cp/ecmwf/python2.5/bin/python2.5
import field_read as flr
import orbit_read as orr
import  bpch2_rw_v2 as brw
import restart_tranform as rtf
import ak_read as akr
from pylab import *
from numpy import *
import time_module as tm
import pres_mod_py as pm
import gp_axis as gax
import obs_operator as obo
import netCDF_gen as nf
import numpy.random as rnd
import state_vector_step as stv_c
import etkf_half as et
import oco_feedback as ofb
import data_collect_step as dcl
import oco_units as ocunit
from Scientific.IO.NetCDF import *

import oco_assim_step_x as ost
import geos_chem_def as gcdf
write_to_array_file=False  # turn off the output the array files

ocs=ost.oco_assim_step()
for i in range(0, 12):

    flnm_x=r'tx_%3.3d.dat' % (i)
    flnm_x=gcdf.inv_path+flnm_x
    flnm_x0=r'tx0_%3.3d.dat' % (i)
    flnm_x0=gcdf.inv_path+flnm_x0
    flnm_dx=r'tdx_%3.3d.dat' % (i)
    flnm_dx=gcdf.inv_path+flnm_dx
    
    sstep=r'%2.2d' % (i)
    
    resflnm=gcdf.inv_path+"p0_oco_assim_res"+"."+ocs.select_mode+"_"+sstep+".nc"
    # resflnm=gcdf.inv_path+"z4_oco_assim_res"+"."+sstep+".nc"
    ocs.do_one_step(update_step=0, rerun_step=0)
    nst=ocs.cur_step
    xstep=arange(ocs.cur_step)
    
    xne=arange(ocs.ne)
    xnx=arange(ocs.nx)
    dimnames=['nx', 'ne', 'nst']
    dimvars=[xnx, xne, xstep]
    dimtypes=['i', 'i', 'i']
    print ocs.ne, ocs.nx
    print shape(ocs.xtm)
    print shape(ocs.dx)
    
    xtm_info=ofb.geos_varinfo('sum_xtm', 'f', ['ne', 'ne'], ocs.xtm)
    dx_info=ofb.geos_varinfo('dx', 'f', ['nx', 'ne'], ocs.dx)
    dx0_info=ofb.geos_varinfo('dx0', 'f', ['nx', 'ne'], ocs.dx0)
    x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    x0_info=ofb.geos_varinfo('x0', 'f', ['nx'], ocs.mean_x0)
    doy_info=ofb.geos_varinfo('doy', 'i', ['nst'], ocs.st_doy[0:nst]) # doy for emission period 
    yyyy_info=ofb.geos_varinfo('yyyy', 'i', ['nst'], ocs.st_yyyy[0:nst])  # year for emission period
    
    
    # x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    # ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, [x_info, dx_info, xtm_info])
    
    ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, \
                             [dx_info, dx0_info, xtm_info, \
                              x_info, x0_info,\
                              yyyy_info, doy_info])
    
    
    if (write_to_array_file):
        ocs.mean_x.tofile(flnm_x,  sep="", format="%s")
        ocs.mean_x0.tofile(flnm_x0,  sep="", format="%s")
        ocs.dx.tofile(flnm_dx,  sep="", format="%s")
    
        

                                                                
