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
import etkf_cor as etc

# import etkf_diag as et

import oco_feedback as ofb
import data_collect_step as dcl
import oco_units as ocunit
from Scientific.IO.NetCDF import *
import geos_chem_def as gcdf 
import read_stn_obs_year as robs_m
import flib as flb
import co2_jacobian as co2j
import numpy.linalg as nlg

class oco_obs_gen:
    def __init__(self, cur_yyyy, doy_st, doy_end, rerun_st=1, rerun_end=2):
        self.rerun_est=rerun_st
        self.rerun_eend=rerun_end
        self.rerun_datapath=gcdf.data_path
        
        self.cur_yyyy=cur_yyyy
        
        viewmode_nadir=['nadir']*16
        viewmode_glint=['glint']*16
        

        if (gcdf.view_mode=='nadir'):
            viewmode_list=viewmode_nadir+viewmode_nadir
            
        elif (gcdf.view_mode=='glint'):
            viewmode_list=viewmode_glint+viewmode_glint

        else:
            viewmode_list=viewmode_nadir+viewmode_glint
            
        viewmode_list=viewmode_list*12
        viewmode_code=list()
        
        for idoy in range(doy_st, doy_end+1):
            yyyy, mm,dd=tm.doy_to_time_array(idoy, self.cur_yyyy)
            sdate=r'%4.4dD%3.3d' % (yyyy, idoy)
            viewmode=viewmode_list[idoy-1]
            ncflnm="./"+gcdf.view_type+"_"+viewmode+"."+sdate+".nc"
            org_ncflnm=gcdf.obs_path+"/"+gcdf.view_type+"_"+viewmode+"."+sdate+".nc"
            print ncflnm
            
            varnames=['time', 'obs_lvl', 'lon', 'lat', 'cloud', 'nclear', 'xco2', 'xco2_ap', \
                      'err', 'rnd_err', \
                      'od', 'lwi', 'sza', 'obs_pres', 'obs_ak', 'obs_apr']
            
            
            time, obs_lvl, lon, lat, cloud, nclear, xco2, xco2_ap, \
                  err, rnd_err, \
                  od, lwi, sza, obs_pres, obs_ak, obs_apr=\
                  ofb.ncf_read(org_ncflnm, varnames)
            
            nobs=size(lat)
            
            self.olat=array(lat)
            self.olon=array(lon)
            self.otime=array(time)
            self.obs_ak=array(obs_ak)
            self.obs_apr=array(obs_apr)
            self.obs_xgp0=array(xco2_ap)
            self.obs_pres=array(obs_pres)
            
            
            
            hm0=self.read_new_mean_y(yyyy, mm, dd)
             
            hm0=squeeze(hm0)
            if (max(hm0)>1.0):
                hm0=1.0e-6*hm0
            
            dimnames=['time', 'obs_lvl']
            dimtypes=['f', 'i']
            dimvars=[time, obs_lvl]
            
            lon_info=ofb.geos_varinfo('lon', 'f', ['time'], lon)
            lat_info=ofb.geos_varinfo('lat', 'f', ['time'], lat)
            cloud_info=ofb.geos_varinfo('cloud', 'f', ['time'], cloud)
            nclear_info=ofb.geos_varinfo('nclear', 'f', ['time'], nclear)
            xco2_info=ofb.geos_varinfo('xco2', 'f', ['time'], hm0)
            xco2_ap_info=ofb.geos_varinfo('xco2_ap', 'f', ['time'], xco2_ap)
            err_info=ofb.geos_varinfo('err', 'f', ['time'], err)
            rnd_err_info=ofb.geos_varinfo('rnd_err', 'f', ['time'], rnd_err)
            od_info=ofb.geos_varinfo('od', 'f', ['time'], od)
            lwi_info=ofb.geos_varinfo('lwi', 'f', ['time'], lwi)
            sza_info=ofb.geos_varinfo('sza', 'f', ['time'], sza)
            
            obs_pres_info=ofb.geos_varinfo('obs_pres', 'f', ['time', 'obs_lvl'], obs_pres)
            obs_ak_info=ofb.geos_varinfo('obs_ak', 'f', ['time', 'obs_lvl'], obs_ak)
            obs_apr_info=ofb.geos_varinfo('obs_apr', 'f', ['time', 'obs_lvl'], obs_apr)
            
            
            ofb.ncf_write_by_varinfo(ncflnm, dimnames, dimtypes, dimvars, [lon_info, lat_info, cloud_info, \
                                                                           nclear_info, xco2_info, xco2_ap_info, \
                                                                           err_info, rnd_err_info, \
                                                                           od_info, lwi_info, sza_info, obs_pres_info, obs_ak_info, obs_apr_info])
            

    def read_new_mean_y(self, yyyy, mm, dd, do_update=True):
        # import co2_jacobian as ddcl
        new_y0=co2j.xco2jacob_sel(yyyy, mm, dd, \
                                  self.olon, self.olat, self.obs_pres, self.obs_ak,\
                                  [self.rerun_est],[self.rerun_eend],\
                                  sel_em=1,\
                                  mod_offset=333.0e-6,\
                                  datapath=self.rerun_datapath,\
                                  do_debug_jco2=False)
        
        # print new_y0
        
        return new_y0
    
if (__name__=='__main__'):
    tz=oco_obs_gen(2006, 5, 365)
    
