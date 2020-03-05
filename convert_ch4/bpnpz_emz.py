from numpy import *
import time_module as tm
import bpch2_rw_vz as brw
from pylab import *
import sys
import numpy as npy
from numpy import *
import time

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
    
    # print 'Read tracer data from',   full_flnm
    
    # print ftraceinfo
    # print  fdiaginfo
    
    bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", \
                               do_read=1,  ftracerinfo=ftraceinfo,\
                               fdiaginfo=fdiaginfo)
    
    # print 'tracer number', bpch2_ts.ntracers
    
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
    
    # print len(data_list)
    bpdata=data_list[0]
    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
   
    
    all_data=list()
    for bpdata in data_list:
    
        all_data.append(bpdata.data)
    
    all_data=npy.array(all_data)
    # print npy.shape(all_data)
    # print 'save'
    
    co2=all_data
    
    categorys=None
    tracers=None
    tranames=['PSURF']
    taus=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    
    for bpdata in data_list:
        tn=bpdata.get_attr(['name'])
        gpname=tn[0].strip()

        gp=bpdata.data

        if (gpname=='PSURF'):
            sp=array(gp)
        elif (gpname=='AVGW'):
            h2o=array(gp)
    h2o=array(co2[0,:,:,:])
    h2o[:,:,:]=1.0e-8
    
    # write to netcdf 
    
    return rlon, rlat, rz, co2,h2o, sp


def convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                  em_st, em_end, inpath, outpath, refval=100e-6):
    """
    convert ensemble files to netcdf 
    
    """
    
    days=[31,28,31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    prefix="ts_satellite"
    
    
    for imm_st in range(month_st, month_end+1):
     
        #S 1:  find starting and ending month for each step 
        
        mn_st=imm_st
        
        mn_end=mn_st+nsteps
        step=mn_st-1
        
        sem=r'ST%3.3d.EN%4.4d-EN%4.4d' % (step, em_st, em_end)
        
        mlist=range(mn_st,mn_end) # ond
        
        # S2: loop over each month 
        
        for mm in mlist:
            m=mm
            yyyy=yyyy_st
            
            if (m>12):
                m=m-12
                yyyy=yyyy_st+1
        
            days_in_month=days[m-1]
            if (mod(yyyy, 4)==0):
                if (m==2):
                    days_in_month=29
            
            if (m==12):
                break
            

            daylist=arange(1, days_in_month+1)
            
            do_split=True
            
            # S3: loop over each day in the month 
            for day in daylist:
                
                sdate=r'%4.4d%2.2d%2.2d' % (yyyy, m, day)
                # T1: read in data from bpch2 file 
                rlon, rlat, rz, co2, h2o, sp=convert_geos_chem_field(yyyy, m, day, step, \
                                                                         em_st, em_end,datapath=inpath)
                gzflnm=outpath+"/"+prefix+"."+sem+"."+sdate+".aux"
                npy.savez(gzflnm, h2o=h2o, sp=sp, lon=rlon, lat=rlat)
                ref_val=co2[0,:,:,:]
                print shape(co2)
                co2_hm=co2[1:,:,:,:]-ref_val[newaxis, :,:,:]
                print amax(co2), amin(co2)
                
                print 'max min co2 ref:',1.0e6*amax(ref_val), 1.0e6*amin(ref_val)
                print 'max min co2_hm:',1.0e6*amax(co2_hm), 1.0e6*amin(co2_hm)
                
                co2_hm=1.0e9*co2_hm
                co2_hm=co2_hm.astype(integer)
                print 'max min co2:',amax(co2_hm), amin(co2_hm)
                gzflnm=outpath+"/"+prefix+"."+sem+"."+sdate
                npy.savez_compressed(gzflnm, co2=co2_hm, lon=rlon, lat=rlat)
                
                # npy.savez_compressed(gzflnm, co20=co2[0,:,:,:], co2=co2, h2o=h2o, sp=sp, lon=rlon, lat=rlat)







                
def convert_em_file_to_netcdf_sel_days(yyyy_lst, mm_lst, day_lst, \
                                           step, em_st, em_end, \
                                           inpath, outpath, refval=100e-6, \
                                           prefix="ts_satellite"):
    
    """
    convert ensemble files to netcdf 
    
    """
    iday=0
    nday=len(day_lst)
    sem=r'ST%3.3d.EN%4.4d-EN%4.4d' % (step, em_st, em_end)
    
    for iday in range(nday):
        yyyy=yyyy_lst[iday]
        
        mm=mm_lst[iday]
        day=day_lst[iday]
        
        sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, day)
        # T1: read in data from bpch2 file 
        rlon, rlat, rz, co2, h2o, sp=convert_geos_chem_field(yyyy, mm, day, step, \
                                                                 em_st, em_end,datapath=inpath)
        gzflnm=outpath+"/"+prefix+"."+sem+"."+sdate+".aux"
        npy.savez(gzflnm, h2o=h2o, sp=sp, lon=rlon, lat=rlat)
        ref_val=co2[0,:,:,:]
        print shape(co2)
        co2_hm=co2[1:,:,:,:]-ref_val[newaxis, :,:,:]
        print amax(co2), amin(co2)
        
        print 'max min co2 ref:',1.0e6*amax(ref_val), 1.0e6*amin(ref_val)
        print 'max min co2_hm:',1.0e6*amax(co2_hm), 1.0e6*amin(co2_hm)
    
        co2_hm=1.0e9*co2_hm
        co2_hm=co2_hm.astype(integer)
        print 'max min co2:',amax(co2_hm), amin(co2_hm)
        gzflnm=outpath+"/"+prefix+"."+sem+"."+sdate
        npy.savez_compressed(gzflnm, co2=co2_hm, lon=rlon, lat=rlat)
                
# npy.savez_compressed(gzflnm, co20=co2[0,:,:,:], co2=co2, h2o=h2o, sp=sp, lon=rlon, lat=rlat)




if (__name__=='__main__'):
    
     inpath='/data/lfeng/oco2_project/enkf_oco2_co2_4/enkf_output/'
     outpath='/data/lfeng/oco2_project/enkf_oco2_co2_4/enkf_output_nc/'
     mm_lst=[3]*31
     day_lst=range(1, 32)
     yyyy_lst=[2015]*31
     
     
     
     for step in range(11, 12):
         
         for select_part in range(1, 6):

             if (select_part==1):
                 
                 # job 1
                 em_st, em_end=1, 77
                 
             elif (select_part==2):
                 
                 # job 1
                 em_st, em_end=77, 153
                 
                 
             elif (select_part==3):
                 
                 # job 1
                 em_st, em_end=153, 229
    

             elif (select_part==4):
                 
                 # job 1
                 em_st, em_end=229, 305
             else:
                 em_st, em_end=305, 366
        
         
             
             convert_em_file_to_netcdf_sel_days(yyyy_lst, mm_lst, day_lst, \
                                                    step, em_st, em_end, \
                                                    inpath, outpath, refval=100e-6)
     
             


                
                
                    
                
                
    
            
    

                

        
            
    
