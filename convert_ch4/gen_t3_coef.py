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

def gen_transcom_coef(flnm, flux_name,\
                      yyyy,\
                      inv_step,\
                      inv_path=gcdf.inv_path,\
                      modelname='GEOS4', \
                      category='CO2-SRCE', ntracer=1, \
                      do_debug=True, \
                      test_month=0):
    
    print flnm
    ext1=bpy.get_name_ext_2d()
    ext1=ext1.strip()
    model_res=bpy.get_res_ext()
    model_res=model_res.strip()
    
    # model information
    
    gc_lon=cmgrd.get_model_lon(model_res=model_res)
    ix=size(gc_lon)
    gc_lat=cmgrd.get_model_lat(model_res=model_res)
    iy=size(gc_lat)
    
    reg_m=rco2_f.read_region_map()
    reg_m=squeeze(reg_m)
    
    nreg=max(reg_m.flat)+1
    coef_m=zeros(shape(reg_m), float)
    sstep=r'%2.2d' % (inv_step)
    
    resflnm=inv_path+"std_oco_assim_res"+"."+sstep+".nc"
    print resflnm
    
    varnames=['whole_x', 'whole_x0', 'dx', 'sum_xtm']
    x, x0, dx, xtm=ofb.ncf_read(resflnm, varnames)
    coef_a=x-x0

    if (test_month>0):
        stest_month=r'%2.2d' % (test_month-1)
        resflnm=inv_path+"/"+"std_oco_assim_res"+"."+stest_month+".nc"
        print resflnm
        x_t, x0_t, dx_t, xtm_t=ofb.ncf_read(resflnm, varnames)
        coef_t=x_t-x0_t
    
    
    nx=nreg-1
    nst=(yyyy-2004)*12*nx
    
    for imm in range(1, 13):
        
        # read biomass_burning  in regular grid box 
        # covert to ktC /y
        
        coef_cut=coef_a[nst:nst+nx]
        coef_m[:,:]=0
        if (imm<=test_month):
            coef_cut=coef_t[nst:nst+nx]
        
        
        for ireg in range(1, nreg):
            sel_cells=where(reg_m==ireg)
            coef_m[sel_cells]=coef_cut[ireg-1]
        
        tau0   = tm.get_tau(yyyy, imm, 1)
        tau0=tau0/3600.0
        
        if (imm<12):
            tau1     = tm.get_tau(yyyy, imm+1, 1)
        else:
            tau1     = tm.get_tau(yyyy+1, 1, 1)
        
        tau1=tau1/3600.0
        sdate=r'%4.4d%2.2d' % (yyyy,imm)
        
        full_flnm=flux_name+"."+sdate
        funit=wfbp.open_flux_bpch2_file(full_flnm, title='flux')
        unit='unitless'
        
        
        wfbp.write_flux_record(funit, coef_m, \
                               gc_lon, gc_lat,\
                               tau0, tau1,\
                               ntracer, \
                               modelname,\
                               category,\
                               unit, \
                               do_debug=False)

        wfbp.close_flux_bpch2_file(funit)
        nst=nst+nx
        
if (__name__=='__main__'):
    sel_yyyys=[2004, 2005, 2006]
    for yyyy in sel_yyyys:
        
        flnm="input.new.dat"
        flux_name='t3reg.coef'
        inv_step=35
        gen_transcom_coef(flnm, flux_name,\
                          yyyy,\
                          inv_step,\
                          modelname='GEOS4', \
                          inv_path='./oco_inv/',\
                          category='CO2-SRCE', ntracer=1, \
                          do_debug=False,\
                          test_month=0)
    
    
    
    
    
