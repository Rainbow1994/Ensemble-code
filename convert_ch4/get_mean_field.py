""" set up jacobian for monthly co inversion
"""
from pylab import *
import bpch2_rw_v2 as brw # need to handle the data
import gp_axis as gax
import gp_field as gf
import geo_constant as gc
import geos_chem_def as gcdf
import time_module as tmdl
import pres_mod_py as pm
import gen_plots as gpl
import field_read as frd
import flib as flb
import oco_feedback as ofb
from numpy import *
import time_module as tm

def read_daily_field(yyyy, mm, dd, \
                     em_st, em_end,\
                     gpcategory=["IJ-AVG-$"],\
                     gpnames=None,\
                     gptracers=None,\
                     datapath=gcdf.data_path, \
                     prefix="ts_24h_avg"):
    
    """ set up  the model fields from time-series files and ctm files
    
    yyyy, mm, dd            ----in-----    year, month, day
    
    em_st_list, em_end_list ----in---  list of the output tagged tracers.
    The name for time series files is in the format of ts.EN[emst]-EN[emend].[date].bpch

    
    datapath  ------ in -----------   directory of the model outputs
    
    gf ----- out  ----- collection of the tagged tracers + surface pressure (SP) + Land MAP(LWI)+Aux data
    
    nem ----- out -----  the number of tagged tracers
    
    """
    
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    iem=1
    
    syyyy=r'%4.4d' % yyyy
    
    sem=r'EN%4.4d-EN%4.4d' % (em_st, em_end)
    full_datapath=datapath
    
    full_flnm=full_datapath+"/"+prefix+"."+sem+"."+sdate+".bpch"

    ftraceinfo=full_datapath+"/"+"tracerinfo"+"."+sem+".dat"
    fdiaginfo=full_datapath+"/"+"diaginfo"+"."+sem+".dat"
    
    bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", \
                               do_read=1,  ftracerinfo=ftraceinfo,\
                               fdiaginfo=fdiaginfo)
    


    # temperature

    categorys=["DAO-3D-$"]
    tracers=None
    tranames=None 
    taus=None
    data_list=None
    
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    print 'found temperature', founded, len(data_list)
    
    bpdata=data_list[0]

    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
    
    t=array(bpdata.data)
    

    # sp 

    categorys=['PS-PTOP']
    
    tracers=None
    tranames=None
    taus=None
    data_list=None
    
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    print 'found sp', founded, len(data_list)
    
    bpdata=data_list[0]
    sp=array(bpdata.data)
    
    
    # gp

    tracers=gptracers
    tranames=gpnames
    
    categorys=gpcategory
    
    taus=None
    data_list=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    
    print 'found gp', founded, len(data_list)
    
          
    
    
    gp_list=list()
    nusd_data=len(data_list)
    
    for idata in range(0, nusd_data):
        bpdata=data_list[idata]
        gp_list.append(bpdata.data)
                
          
    return rlon, rlat, rz, t, sp, gp_list



    
    # add the standard one

if (__name__=='__main__'):
    yyyy=2006
    for mm in range(1, 13):
        
        doy_st=tm.day_of_year(yyyy, mm, 1)
        if (mm<12):
            doy_end=tm.day_of_year(yyyy, mm+1, 1)
            doy_end=doy_end-1
            
        else:
            doy_end=tm.day_of_year(yyyy, mm, 31)
            doy_end=doy_end

    

    
        sdate=r'%4.4d%2.2d' % (yyyy, mm)
    
        ndays=doy_end-doy_st+1
        em_st, em_end=1,2 
        
        datapath="/home/lfeng/local_disk_2/tag_co2/run4_nep_cp/run_"+str(yyyy)+"_new/"
        
        for idoy in range(doy_st, doy_end+1):
            yyyy, mm, dd=tm.doy_to_time_array(idoy, yyyy)
        
            lon, lat, z, cur_t, cur_sp, data_list= read_daily_field(yyyy, mm, dd, \
                                                                    em_st, em_end, \
                                                                    gpcategory=["IJ-AVG-$"],\
                                                                    gpnames=None,\
                                                                    gptracers=None ,\
                                                                    datapath=datapath)
            
            val1=1.0e6*data_list[0]
            val2=1.0e6*data_list[1]
            
            if (idoy==doy_st):

                sp=array(cur_sp)
                t=array(cur_t)
                data0=array(val1)
                data1=array(val2)
            else:
                
                data0=data0+array(val1)
                data1=data1+array(val2)
                sp=sp+cur_sp
                t=t+cur_t
            
        y0=data0/ndays
        y1=data1/ndays
        sp=sp/ndays
        sp=squeeze(sp)
        t=t/ndays
        
        nx, ny,nz=shape(t)
        
        print size(lon), size(lat), size(z)
        print shape(sp), shape(t)
        
        dimnames=['lon', 'lat', 'z']
        
        dimvars=[lon, lat,z]
        dimtypes=['f', 'f','f']
        outflnm='mean_field_orch.'+sdate+".nc"
        
        y0_info=ofb.geos_varinfo('CO2.0001', 'f', ['lon', 'lat', 'z'], y0, \
                                 varattr={"unit":"ppmv", "desc":"CO2 mixing ratio"})
        
        y1_info=ofb.geos_varinfo('CO2.0002', 'f', ['lon', 'lat','z'], y1, \
                                 varattr={"unit":"ppmv", "desc":"CO2 mixing ratio"})
        
        sp_info=ofb.geos_varinfo('pressure', 'f', ['lon', 'lat'], sp, \
                                 varattr={"unit":"hPa", "desc":"surface pressure"})
        
        t_info=ofb.geos_varinfo('t', 'f', ['lon', 'lat', 'z'], t, \
                                varattr={"unit":"K", "desc":"temperature"})
        
        ofb.ncf_write_by_varinfo(outflnm, dimnames, dimtypes, dimvars,\
                                 [sp_info,y0_info, y1_info, t_info])
        

    

    
    
    
