# import regrid_py as rgp
import oco_units as ocu
import oco_feedback as ofb
from numpy import *
import write_flux_bpch as wfbp
import geo_constant as gc
import gen_plots as gpl
import time_module as tm
import read_co2_flux as rco2_f
import geos_chem_def as gcdf
import compute_model_grid as cmgrd
import bpch2_rw_py as bpy

def gen_transcom_coef(flux_name,\
                      yyyy,\
                      coef_a,\
                      inv_step,\
                      inv_path=gcdf.inv_path,\
                      modelname='GEOS5', \
                      category='CO2-SRCE', ntracer=1, \
                      do_debug=True, \
                      test_month=0):
    
    # print flnm
    ext1=bpy.get_name_ext_2d()
    ext1=ext1.strip()
    model_res=bpy.get_res_ext()
    model_res=model_res.strip()
    
    # model information
    
    gc_lon=cmgrd.get_model_lon(model_res=model_res)
    ix=size(gc_lon)
    gc_lat=cmgrd.get_model_lat(model_res=model_res)
    iy=size(gc_lat)
    
    reg_m=rco2_f.read_region_map('2006D001')
    reg_m=squeeze(reg_m)
    
    nreg=max(reg_m.flat)+1
    coef_m=zeros(shape(reg_m), float)
   
    
    
    # nx=nreg # -1
    # nst=(yyyy-2003)*12*nx
    nst=0
    idoy=1
    nstep=inv_step
    
    print 'nstep, nreg', nstep, nreg
    

    inc_doy=8
    
    for istep in range(0, nstep):
        
        # read biomass_burning  in regular grid box 
        # covert to ktC /y
        
        coef_cut=coef_a[nst:nst+nreg]
        coef_m[:,:]=0
        sdoy=r'%4.4dD%3.3d' % (yyyy,idoy)
        
        reg_flux=rco2_f.read_reg_flux_map(sdoy)
        print shape(reg_flux)
        
        for ireg in range(nreg):
            coef_m[:,:]=coef_m[:,:]+coef_cut[ireg]*reg_flux[:,:, ireg]
        
        
        yyyy, mm, dd=tm.doy_to_time_array(idoy, yyyy)
        tau0   = tm.get_tau(yyyy, mm, dd)
        tau0=tau0/3600.0

        idoy=idoy+inc_doy
        yyyy, mm, dd=tm.doy_to_time_array(idoy, yyyy)
        tau1     = tm.get_tau(yyyy, mm, dd)
        tau1=tau1/3600.0
        
        
        full_flnm=flux_name+sdoy
        funit=wfbp.open_flux_bpch2_file(full_flnm, title='flux')
        unit='kg/s'
        print '--------sum--------'
        print 'step:', istep
        
        print 'max, min adjustment (GtC/a):', ocu.kg_s_to_GtC_Y*max(coef_m.flat), ocu.kg_s_to_GtC_Y*min(coef_m.flat)
        print 'total adjustment (GtC/a):', ocu.kg_s_to_GtC_Y*sum(coef_m)

        print 'max, min adjustment (kg/s):', max(coef_m.flat), min(coef_m.flat)
        print 'total adjustment (kg/s):', sum(coef_m)
        
        print '--------end--------' 
        
        wfbp.write_flux_record(funit, coef_m, \
                               gc_lon, gc_lat,\
                               tau0, tau1,\
                               ntracer, \
                               modelname,\
                               category,\
                               unit, \
                               do_debug=False)

        wfbp.close_flux_bpch2_file(funit)
        nst=nst+nreg
        
        
if (__name__=='__main__'):
    yyyy=2006

    inv_step=17
    inv_path='./oco_inv_tight_noshape/'
    sstep=r'%2.2d' % (inv_step)
    sstep=r'%2.2d' % inv_step
    
    resflnm=inv_path+"std_oco_assim_res"+"."+sstep+".nc"
    print resflnm
    

    do_pertb=True
    
    if (do_pertb):
        
        coef_a=zeros(inv_step*144, float)
        coef_a[1:19]=0.2
        coef_a[82:100]=0.0
    else:
        varnames=['whole_x', 'whole_x0', 'dx', 'sum_xtm']
        x, x0, dx, xtm=ofb.ncf_read(resflnm, varnames)
        coef_a=x-x0
        
    flux_output_name='CO2_EMISSION_PERTURB'
        
    gen_transcom_coef(flux_output_name,\
                      yyyy,\
                      coef_a,\
                      inv_step,\
                      inv_path='./oco_inv_tight_shape/',\
                      modelname='GEOS5', \
                      category='CO2-SRCE', ntracer=1, \
                      do_debug=False)
    
    
    
    
    
