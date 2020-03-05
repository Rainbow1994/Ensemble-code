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
import sys
import numpy as npy
import save_test as svt
import gzip

def convert_geos_chem_field(yyyy, mm, dd, \
                                step,\
                                em_st,\
                                em_end,\
                                modtype=5,\
                                datapath="../enkf_new_2010/enkf_output/" \
                                ):
    
    # read in the GEOS-Chem model data
    
    
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    figdoy=tm.day_of_year(yyyy, mm, dd)
    # sdoy=r'%3.3d' % (doy)
    sem=r'ST%3.3d.EN%4.4d-EN%4.4d' % (step, em_st, em_end)
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
    
    # extract co2 data set
    
    categorys=None
    tracers=None
    tranames=['CO2']
    taus=None
    data_list=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    
    
    all_data=list()
    for bpdata in data_list:
    
        all_data.append(bpdata.data)
    
    all_data=npy.array(all_data)
    print npy.shape(all_data)
    print 'save'
    
    all_data=1.0e10*all_data
    all_data=all_data-100.0e4
    all_data=all_data.astype(integer)
    fd=gzip.open('test2.bin', 'wb')
    fd.write(all_data)
    
    
    npy.save('test_npy', all_data)
    print 'Done 1'
    
    svt.save_array(all_data)
    print 'Done 2'
    
if (__name__=='__main__'):
    mlist=range(1, 13)
    for m in mlist:
        days=[31,28,31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (m==1):
            daylist=arange(1, days[m-1]+1)
        else:
            daylist=arange(1, days[m-1]+1)
        
        for day in daylist:
            convert_geos_chem_field(2010, 4, 30, 0, 1, 102)
            kkk=raw_input()
            
            
    
