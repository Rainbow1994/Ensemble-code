#! /geos/u23/epd/bin/python2.5
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
import geos_chem_def as gcdf

import oco_assim_step as ost
ocs=ost.oco_assim_step()

for i in range(0, 20):
    sstep=r'%2.2d' % (i)
    resflnm=gcdf.inv_path+"/"+"std_oco_assim_res"+"."+sstep+".nc"
    ocs.do_one_step(update_step=0, rerun_step=0, hm_saving_doy=0)
    xne=arange(ocs.ne)
    xnx=arange(ocs.nx)
    xwhole=arange(size(ocs.whole_mean_x))
    dimnames=['nx', 'ne', 'nwhole']
    dimvars=[xnx, xne, xwhole]
    dimtypes=['i', 'i', 'i']
    # print ocs.ne, ocs.nx
    # print shape(ocs.xtm)
    # print shape(ocs.dx)
    
    # out put to the restart file

    xtm_info=ofb.geos_varinfo('sum_xtm', 'f', ['ne', 'ne'], ocs.xtm)
    x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    xinc_info=ofb.geos_varinfo('xinc', 'f', ['nx'], ocs.x_inc)

    x0_info=ofb.geos_varinfo('x0', 'f', ['nx'], ocs.mean_x0)
    whole_x0_info=ofb.geos_varinfo('whole_x0', 'f', ['nwhole'], ocs.whole_mean_x0)
    whole_x_info=ofb.geos_varinfo('whole_x', 'f', ['nwhole'], ocs.whole_mean_x)
    
    whole_err0_info=ofb.geos_varinfo('whole_err0', 'f', ['nwhole'], ocs.whole_err_x0)
    whole_err_info=ofb.geos_varinfo('whole_err', 'f', ['nwhole'], ocs.whole_err_x)

    
    print shape(ocs.whole_err_x)
    print shape(ocs.whole_err_x0)
    
    dx_info=ofb.geos_varinfo('dx', 'f', ['nx', 'ne'], ocs.dx)

    # flux

    dx_flux_info=ofb.geos_varinfo('dx_flux', 'f', ['nx'], ocs.dx_flux)
    
    flux_info=ofb.geos_varinfo('flux', 'f', ['nx'], ocs.mean_flux)

    
    flux0_info=ofb.geos_varinfo('flux0', 'f', ['nx'], ocs.mean_flux0)
    whole_flux0_info=ofb.geos_varinfo('whole_flux0', 'f', ['nwhole'], ocs.whole_mean_flux0)
    whole_flux_info=ofb.geos_varinfo('whole_flux', 'f', ['nwhole'], ocs.whole_mean_flux)
    
    whole_flux_err0_info=ofb.geos_varinfo('whole_flux_err0', 'f', ['nwhole'], ocs.whole_err_flux0)
    whole_flux_err_info=ofb.geos_varinfo('whole_flux_err', 'f', ['nwhole'], ocs.whole_err_flux)
    whole_dx_flux_info=ofb.geos_varinfo('whole_dx_flux', 'f', ['nwhole'], ocs.whole_dx_flux)
    
    
    print shape(ocs.whole_err_x)
    print shape(ocs.whole_err_x0)
    
    dx_info=ofb.geos_varinfo('dx', 'f', ['nx', 'ne'], ocs.dx)

    
    
    # x_info=ofb.geos_varinfo('x', 'f', ['nx'], ocs.mean_x)
    # ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, [x_info, dx_info, xtm_info])
    
    ofb.ncf_write_by_varinfo(resflnm, dimnames, dimtypes, dimvars, [dx_info, xtm_info, x_info, \
                                                                    x0_info, xinc_info, \
                                                                    whole_x_info, whole_x0_info,\
                                                                    whole_err_info, whole_err0_info,\
                                                                    dx_flux_info,\
                                                                    flux_info, flux0_info, \
                                                                    whole_flux_info, whole_flux0_info,\
                                                                    whole_flux_err_info, \
                                                                    whole_flux_err0_info, \
                                                                    whole_dx_flux_info\
                                                                    ])
    
    
    

                                                                
