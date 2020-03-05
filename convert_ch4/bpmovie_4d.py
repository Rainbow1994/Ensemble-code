from numpy import *
import time_module as tm
import gp_axis as gax
import flib
import oco_feedback as ofb
import pres_mod_py as pm
import bpch2_rw_v2_wx as brw
import compute_model_grid as cmg
import gen_plots as gpl
from pylab import *

def convert_geos_chem_field(yyyy, mm, dd, \
                         modtype=5,\
                         datapath="./enkf_output_g5" \
                            ):
    
    # read in the GEOS-Chem model data
    
    
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    figdoy=tm.day_of_year(yyyy, mm, dd)
    # sdoy=r'%3.3d' % (doy)
    em_st=1
    em_end=2 
    sem=r'EN%4.4d-EN%4.4d' % (em_st, em_end)
    full_flnm=datapath+"/"+"ts_satellite"+"."+sem+"."+sdate+".bpch"
    ncflnm=datapath+"/"+"ts_satellite"+"."+sdate+".nc"
    
    ftraceinfo=datapath+"/"+"tracerinfo"+"."+sem+".dat"
    fdiaginfo=datapath+"/"+"diaginfo"+"."+sem+".dat"
    
    print 'Read tracer data from',   full_flnm

    print ftraceinfo
    print  fdiaginfo
    
    bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", \
                               do_read=1,  ftracerinfo=ftraceinfo,\
                               fdiaginfo=fdiaginfo)
    
    print 'tracer number', bpch2_ts.ntracers
    
    #  bpch2_ts.print_datainfo()
    # get the total co2
    # CO2 profile
    
    
    categorys=None
    tracers=None
    tranames=['CO2']
    taus=None
    data_list=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    
    print founded, len(data_list)
    # how change tracer number
    #
    # for example, we choose  northern american region 3 
    # bpdata=data_list[3]
    # the 100 ppm backgroundfrom tracer '1'
    #
    # bpdata2=data_list[1]
    # co2=bpdata.data-bpdata2.data
    # or simply 
    # co2=bpdata.data-100.0e-6
    
    
    # the following is a special case when tracer one is coming from posteriori flux adjustment
    
    bpdata=data_list[0]
    bpdata2=data_list[1]
    
    # co2=bpdata.data+bpdata2.data-100.0e-6
    
    
    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
    
    categorys=None
    tracers=None
    tranames=['PSURF', 'AVGW']
    taus=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    
    for bpdata in data_list:
        tn=bpdata.get_attr(['name'])
        gpname=tn[0].strip()

        gp=bpdata.data

        if (gpname=='PSURF'):
            sp=array(gp)
            levels=rz[:]
            levels=array(levels)
            levels=levels+1
            levels=levels.astype(int)
            pres=pm.get_pres_mod_2d(sp, levels, 5, 1)
        elif (gpname=='AVGW'):
            h2o=array(gp)
            
    # write to netcdf 
    
    return figdoy, rlon, rlat, rz, co2, pres, sp

if (__name__=='__main__'):
    from numpy import *
    # months you choose
    mlist=range(1, 2)
    all_doy=list()
    all_co2=list()
    all_pres=list()
    all_sp=list()
    
       
    ncflnm='test_4d.nc'
    
    for m in mlist:
        days=[31,28,31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (m==1):
            daylist=arange(1, days[m-1]+1)
        
        for day in daylist:
            doy,rlon, rlat, rz, co2, pres, sp=convert_geos_chem_field(2006, m, day)
            all_doy.append(doy)
            all_co2.append(co2)
            all_pres.append(pres)
            all_sp.append(squeeze(sp))
        
    
    all_doy=array(all_doy)
    all_co2=array(all_co2)
    all_pres=array(all_pres)
    all_sp=array(all_sp)

    print shape(all_co2), shape(all_sp)
    
    
    

    lat_info=ofb.geos_varinfo('latitude', 'f', ['latitude'], rlat, \
                              varattr=None)
    
    lon_info=ofb.geos_varinfo('longitude', 'f', ['longitude'], rlon, \
                              varattr=None)
    lvl_info=ofb.geos_varinfo('level', 'f', ['level'], rz, \
                              varattr=None)
    
    time_info=ofb.geos_varinfo('time', 'f', ['time'], all_doy, \
                              varattr={"units":"days since 2006-1-1 00:00:00"})
    
                              
                                       
    
    co2=transpose(all_co2, (0,3,2,1))
    pres=transpose(all_pres, (0,3,2,1))
    sp=transpose(all_sp, (0,2,1))
    
    print shape(co2)
    
    
    co2_info=ofb.geos_varinfo('co2', 'f', ['time', 'level', 'latitude', 'longitude'], co2, \
                              varattr={"units":"v/v", "long_name":"CO2 mixing ratio", \
                                       "standard_name":"mole_fraction_of_carbon_dioxide_in_air"})
    
    pres_info=ofb.geos_varinfo('pressure', 'f', ['time','level', 'latitude', 'longitude'], pres,\
                               varattr={"units":"hPa", "long_name":"pressure", \
                                        "standard_name":"air_pressure"})
    
    sp_info=ofb.geos_varinfo('sp', 'f', ['time','latitude', 'longitude'], transpose(sp),\
                             varattr={"units":"hPa", "long_name":"surface pressure", \
                                      "standard_name":"surface_air_pressure"})
    
   
    ofb.ncf_write_cf(ncflnm, [lon_info, lat_info, lvl_info, time_info],\
                     [co2_info, pres_info])
    
    
o
        
            
    
