#! /home/lfeng/epd/bin/python2.5
# from pylab import *
# import bpch2_rw_v2 as brw # need to handle the data
import geo_constant as gc
import geos_chem_def as gcdf # the data path etc 
import time_module as tmdl
import gen_plots as gpl
from numpy import *
import weekly_data_collect as wdcl
import oco_feedback as ofb
import read_stn_obs_year as robs_m

yyyy=2004
syyyy=str(yyyy)
est=1
eend=2
sel_ems=[1,2]
nusd_week=47

# sel_ems=range(1,8)
# sel_ems=array(sel_ems)
ntr=size(sel_ems)


data_path="/home/lfeng/local_disk_2/tagged_co2/run5_em2/run_"+syyyy+"_v8/"

# data_path="/home/lfeng/local_disk_2/tag_co2/run_37_cp/run_"+syyyy+"/"


#data_path=gcdf.data_path+"/"+syyyy+"/" 


# data_path=gcdf.data_path

# data_path="./enkf_output/"

obsflnm="v8_co2_stn_obs"+"."+syyyy+".nc"


# start and end date

# read in the observation data 
flnm_stn_list=robs_m.def_stn_pos_flnm+"_"+str(yyyy)+".txt"

stn_c=robs_m.stn_obs(stn_list=flnm_stn_list, yyyy_st=yyyy, yyyy_end=yyyy)
            
otime, olon, olat, oz, osf, \
            orsd, ow, ouse,\
            nobs, obs, oerr=stn_c.collect_stn_data()

# stn_c=robs_m.stn_obs(yyyy_st=yyyy, yyyy_end=yyyy)

# otime, olon, olat, oz, nobs, obs, oerr=stn_c.collect_stn_data()

nstn=size(olon)


# change from fraction to
if (mod(yyyy, 4)==0):
    odoy=(otime-yyyy)*366
else:
    odoy=(otime-yyyy)*365

odoy=odoy+1.5
odoy=odoy.astype(integer)
nweek=size(odoy)
odoy_end=odoy[-1]
nx,ny=shape(obs)

mod_vals=zeros([nx, ny, ntr], float)

   

for iweek in range(nusd_week):
# for iweek in range(5):

    doy1=odoy[iweek]
    if (doy1==1 and yyyy==-2006):
        doy1=5
        
    doy2=odoy[iweek+1]
    icount=0
    
    
    new_y0=wdcl.get_sel_avg_model_data(otime, olon, olat, oz,\
                                       doy1, doy2, \
                                       est,eend,yyyy,\
                                       sel_ems,\
                                       data_path,\
                                       osf=osf)
    print shape(new_y0)
    
    mod_vals[iweek, 0:nstn,0:ntr]=new_y0[0:nstn, 0:ntr]
    
    
# output obs and model values
nobs, nstn, ntr=shape(mod_vals)
dimnames=['nobs', 'nstn', 'ntr']
xobs=arange(nobs)
xstn=arange(nstn)
xntr=arange(ntr)

dimvars=[xobs, xstn, xntr]
dimtypes=['i', 'i', 'i']


olon_info=ofb.geos_varinfo('lon', 'f', ['nstn'], olon,varattr={"unit":"degree", "desc":"longitude"})
otime_info=ofb.geos_varinfo('time', 'f', ['nstn'], otime,varattr={"unit":"none", "desc":"time idx"})
odoy_info=ofb.geos_varinfo('odoy', 'f', ['nstn'], odoy,varattr={"unit":"day", "desc":" day of year "})
olat_info=ofb.geos_varinfo('lat', 'f', ['nstn'], olat,varattr={"unit":"degree", "desc":"latitude"})
oz_info=ofb.geos_varinfo('oz', 'f', ['nstn'], oz,varattr={"unit":"m", "desc":"height"})


obs_info=ofb.geos_varinfo('obs', 'f', ['nobs', 'nstn'], obs, \
                          varattr={"unit":"ppmv", "desc":"CO2 mixing ratio"})
oerr_info=ofb.geos_varinfo('err', 'f', ['nobs', 'nstn'], \
                           oerr,varattr={"unit":"ppmv*ppmv", "desc":"observation error"} )

y_info=ofb.geos_varinfo('y', 'f', ['nobs', 'nstn','ntr'], mod_vals, \
                          varattr={"unit":"ppmv", "desc":"model CO2 mixing ratio"})

ofb.ncf_write_by_varinfo(obsflnm, dimnames, dimtypes, dimvars,\
                         [olon_info, olat_info, oz_info, odoy_info, \
                          obs_info,\
                          oerr_info,\
                          y_info])







    








