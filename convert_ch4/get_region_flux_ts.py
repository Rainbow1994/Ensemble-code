from pylab import *
from numpy import *
from Scientific.IO.NetCDF import *
import numpy.linalg as nlg
import co2_emission_std as co2em
import oco_units as ocunit
import gen_plots as gpl
import geos_chem_def as gcdf     # deflaut settings
import numpy as np


def get_reg_sum(sel_step,\
                fl_paths=['./oco_inv_prior/', './oco_inv_no_t_cor/', './oco_inv/' ],  \
                output_names=['prior', 'old',  'new'],\
                nreg=144,\
                do_debug=False \
                ):
    
    co2=co2em.transcom_co2_st(sel_id=0, \
                              n_land_lon_div=1,\
                              n_land_lat_div=1,\
                              n_ocean_lon_div=1,\
                              n_ocean_lat_div=1\
                              )

    reg_names=co2.reg_name
    
    lat=co2.lat
    lon=co2.lon
    xnorm=1.0
    
    
    
    
    
    
    nt3_reg=co2.nreg
    t3_sep=zeros(nt3_reg)
    last_nreg=0
    
    for ireg in range(nt3_reg):
        if (ireg==0):
            t3_sep[ireg]=0
            last_nreg=0
        elif (ireg<12): # land region
            t3_sep[ireg]=last_nreg+9
            last_nreg=last_nreg+9
        else:
            t3_sep[ireg]=last_nreg+4
            last_nreg=last_nreg+4

    print  t3_sep

    cur_sep=arange(nreg)
    
    # the table for parent regions
    
    reg_idx_table=searchsorted(t3_sep, cur_sep)
    
    print reg_idx_table
  
    nst=0
    nend=sel_step

    ssel_step=r'%2.2d' % sel_step
    iplot=0
    
    ifl=0
    
    for flnm in fl_paths:
        flnm=flnm+"std_oco_assim_res."+ssel_step+".nc"
        print 'read data from ', flnm
        
        ncf=NetCDFFile(flnm, "r")
        dx=ncf.variables['dx']
        dx=array(dx)
        print shape(dx)
        sum_xtm=ncf.variables['sum_xtm']
        dx=dx*ocunit.kg_s_to_GtC_Y
        xcor0=dot(dx, transpose(dx))
        xcor0=xcor0/xnorm
        
        dx=dot(dx, sum_xtm)
        xcor=dot(dx, transpose(dx))
        xcor=xcor/xnorm
        whole_err=ncf.variables['whole_flux_err']
        whole_err0=ncf.variables['whole_flux_err0']
        whole_err=array(whole_err)
        whole_err0=array(whole_err0)
        
        whole_err=ocunit.kg_s_to_GtC_Y*ocunit.kg_s_to_GtC_Y*array(whole_err)
        whole_err0=ocunit.kg_s_to_GtC_Y*ocunit.kg_s_to_GtC_Y*array(whole_err0)
        
        
        # mean values
        
        mean_x0=ncf.variables['whole_flux0']
        mean_x0=array(mean_x0)
        mean_x0=mean_x0*ocunit.kg_s_to_GtC_Y
        
        
        
        mean_x=ncf.variables['whole_flux']
        mean_x=array(mean_x)
        mean_x=mean_x*ocunit.kg_s_to_GtC_Y

        ncf.close()
        
        
        
        sel1=0
        sel2=1
        ratio=1.0
        
        # print x0[0:5, 0]
        # print x[0:5, 0]
        # nreg=co2.nreg
        nsel=nreg
        
        ist=0
        iend=ist+nreg
        print ist, iend
        
        sum_co2err=zeros([nreg, nreg], float)
        sum_co2err0=zeros([nreg, nreg], float)
        
        sum_x=zeros(nreg, float)
        sum_x0=zeros(nreg, float)
    
        
        ist=nreg*nst
        iend=ist+nreg
        
        t3_x_ts=list()
        t3_x0_ts=list()
        t3_err_ts=list()
        t3_err0_ts=list()
        
        # loop over data set
        doys=list()
        
        for itime in range(nst, nend):
            sel_idx=arange(ist, iend)
            print shape(xcor)
            co2err= whole_err[ist:iend]
            co2err0= whole_err0[ist:iend]

            print 'shape co2err', shape(co2err), ist, iend
        
            
            if (size(co2err)>0):
                sum_co2err=co2err
                sum_co2err0=co2err0
                
                sum_x=mean_x[ist:iend]
                sum_x0=mean_x0[ist:iend]
                
                sum_t3_x=zeros(nt3_reg, float)
                sum_t3_x0=zeros(nt3_reg, float)
                sum_t3_err=zeros(nt3_reg, float)
                sum_t3_err0=zeros(nt3_reg, float)
    
                for ireg in range(nt3_reg):
                    sel_reg_idx=where(reg_idx_table==ireg)
                    sum_t3_x[ireg]=sum(sum_x[sel_reg_idx])
                    sum_t3_x0[ireg]=sum(sum_x0[sel_reg_idx])
                    sum_t3_err[ireg]=sum(sum_co2err[sel_reg_idx])
                    sum_t3_err0[ireg]=sum(sum_co2err0[sel_reg_idx])
                    
                sum_t3_err=sqrt(sum_t3_err)
                sum_t3_err0=sqrt(sum_t3_err0)
                
                t3_x_ts.append(sum_t3_x)
                t3_x0_ts.append(sum_t3_x0)
                t3_err_ts.append(sum_t3_err)
                t3_err0_ts.append(sum_t3_err0)
                doys.append(itime)
                
                    
            ist=iend
            iend=ist+nreg
            
            
        
        t3_x_ts=array(t3_x_ts)
        t3_x0_ts=array(t3_x0_ts)
        t3_err_ts=array(t3_err_ts)
        t3_err0_ts=array(t3_err0_ts)
        doys=array(doys)
        
        print max(t3_x_ts.flat), min(t3_x_ts.flat)
        
        # save the data
        np.save(output_names[ifl]+"_x_ts."+ssel_step, t3_x_ts)
        np.save(output_names[ifl]+"_x0_ts."+ssel_step, t3_x0_ts)
        np.save(output_names[ifl]+"_err_ts."+ssel_step, t3_err_ts)
        np.save(output_names[ifl]+"_err0_ts."+ssel_step, t3_err0_ts)
        np.save(output_names[ifl]+"_doys."+ssel_step, doys)
        ifl=ifl+1
    
    return reg_names

if (__name__=='__main__'):
    sel_step=10
    reg_names=get_reg_sum(sel_step,\
                          fl_paths=['./oco_inv/'], \
                          output_names=['new'],\
                          nreg=144,\
                          do_debug=False \
                          )
    
        

   
        

