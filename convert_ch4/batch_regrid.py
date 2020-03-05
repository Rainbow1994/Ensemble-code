#! /geos/u23/epd/bin/python2.5
from numpy import *

import field_grid as fgrd
import compute_model_grid as cmg
import write_3d_bpch as w3df
import gp_axis as gax
import time_module as tm
# import bpch2_rw_v2_wx as bpch2_mod

def Regrid(bpdata_list,\
           ps,\
           pressure,\
           outfile, \
           mod_res='2x25',\
           mod_type=5):
    
    import field_grid as fgrd
    import compute_model_grid as cmg
    import write_3d_bpch as w3df
    import gp_axis as gax
    
    # mod res
    
    outfile=outfile.strip()
    
    if (mod_type==4):
        nz=30 
    elif (mod_type==5):
        nz=47 # the same as model level 
        
        
    new_lat=cmg.get_model_lat(mod_res)
    new_lon=cmg.get_model_lon(mod_res)
    
   
    funit=w3df.open_3d_bpch2_file(outfile, title='flux', do_ext=False)
    if (mod_type==5):
        ext1='geos5'
    else:
        ext1='geos'
                
    for bpdata in bpdata_list:
        tracerid=bpdata.ntracer
        rlon=bpdata.grid.get_lon()
        rlat=bpdata.grid.get_lat()
        nlon=size(rlon)
        nlat=size(rlat)
        traname, tau0, tau1=bpdata.get_attr(['name', 'tau0', 'tau1'])
        
        ax_lat=gax.gp_axis('lat', rlat)
        ax_lon=gax.gp_axis('lon', rlon)
        
        lonp1, lonp2, lonw=ax_lon.getwgt(new_lon)
        latp1, latp2, latw=ax_lat.getwgt(new_lat)
        
        if (ps<>None):
            new_data1=lonw[:,newaxis]*ps[lonp1, :]+\
                       (1.0-lonw[:,newaxis])*ps[lonp2,:]
        

            new_ps=latw[newaxis, :]*new_data1[:,latp1]+\
                    (1.0-latw[newaxis, :])*new_data1[:,latp2]
        
            new_ps=squeeze(new_ps)
        
        
            new_pres, tmp_ps=fgrd.get_model_pressure(nz, mod_type=mod_type, ps=new_ps, \
                                                     psfile=None, cater_ps='PS',\
                                                     tracer_ps=None, tau_ps=None)
        
            print 'shape new pressure', shape(new_pres)

            
            new_data=fgrd.regrid_data(bpdata.data, rlon, rlat, \
                                      new_lon, new_lat, \
                                      pressure=pressure, new_pres=new_pres)
            print shape(new_data)
        else:
            new_data1=lonw[:,newaxis, newaxis]*bpdata.data[lonp1, :,:]+\
                       (1.0-lonw[:,newaxis, newaxis])*bpdata.data[lonp2,:,:]
        

            new_data=latw[newaxis, :,newaxis]*new_data1[:,latp1,:]+\
                    (1.0-latw[newaxis, :,newaxis])*new_data1[:,latp2,:]
            
            new_data=squeeze(new_data)
        
        print 'new data', shape(new_data), max(new_data.flat), min(new_data.flat)
        print 'origin data', shape(bpdata.data), max(bpdata.data.flat), min(bpdata.data.flat)
            
        w3df.write_3d_field(funit,new_data, \
                            new_lon, new_lat, \
                            tau0, tau1,\
                            bpdata.ntracer, \
                            ext1,\
                            category=bpdata.category,\
                            unit=bpdata.unit, \
                            do_debug=False)
        
    w3df.close_3d_bpch2_file(funit)
        
        
            
        
if (__name__=='__main__'):
    import bpch2_rw_v2 as brw
    
    datapath="./"
    
    # file names to be converted  
    flnm_list=['restart.EN0001-EN0002.2004010100']
    # info files
    
    ftraceinfo="./enkf_output/tracerinfo.EN0001-EN0002.dat"
    fdiaginfo="./enkf_output/diaginfo.EN0001-EN0002.dat"
    old_mod_type=4

    if (old_mod_type==4):
        lx=30
    elif (old_mod_type==5):
          lx=47
    
    #for flnm in flnm_list:
    ps_filename='ts_24h_avg.EN0001-EN0002.20040101.bpch'
    
    for flnm in flnm_list:
            
        full_flnm=datapath+"/"+flnm
            
        outfile=datapath+"/x"+flnm
            
        print '1.============= Read tracer data from',   full_flnm
        print ftraceinfo
        print  fdiaginfo
        
        bpch2_ps=brw.bpch2_file_rw(ps_filename, "r", \
                                   do_read=1, \
                                   ftracerinfo=ftraceinfo,\
                                   fdiaginfo=fdiaginfo)
        
        # surface pressure
        # careful check needed for different GEOS-Chem version 
        
        categorys=['PS-PTOP']
        tracers=None
        
        
        tranames=None 
        taus=None
        data_list=None
        data_list, founded=bpch2_ps.get_data(categorys, tracers, taus, tranames)
        if (len(data_list)<1):
            ps=None
            pressure=None
        else:
            ps=data_list[0].data
            ps=squeeze(ps)
            pressure, new_ps=fgrd.get_model_pressure(lx, mod_type=old_mod_type, ps=ps)
        
        bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", \
                                   do_read=1, \
                                   ftracerinfo=ftraceinfo,\
                                   fdiaginfo=fdiaginfo)
        
        
        categorys=None
        tracers=None
        tranames=None
        taus=None
        data_list=None
        data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
            
        
        print '2. ================= Write tracer data to',   outfile
        Regrid(data_list,\
               ps,\
               pressure,\
               outfile, \
               mod_res='4x5',\
               mod_type=5)

            
            
            
