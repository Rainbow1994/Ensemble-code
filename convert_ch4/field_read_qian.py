from numpy import *
import bpch2_rw_v2 as brw # need to handle the data
import gp_axis as gax
import gp_field as gf
import geo_constant as gc
import geos_chem_def as gcfs
import time_module as tm
import pres_mod_py as pm

def get_col_wgt(pres):
    """ the weight factor for integration 
        Arguments:
            pres    :   pressure given as log10(pressure) from top of mode to surface
        Returns:
            wgt     : weighting factor for each level
    """
    
    if (max(pres)>10):
        pres_a=array(pres)
        pres=log10(pres)
    else:
        pres_a=10.0**(pres)
    sum_wgt1=pres_a[1:]-pres_a[0:-1]
    sum_wgt0=0.5*(pres_a[2:]-pres_a[0:-2])
    sum_wgt0=sum_wgt0/(pres_a[-1]-pres_a[0])
    
    sum_wgt2=pres[1:]-pres[:-1]
    sum_wgt2=log(10.0)*sum_wgt2
    fsum=sum_wgt1/sum_wgt2
    sum_wgt=fsum[1:]-fsum[:-1] # the weight factor as (p(k+1)-p(k))/log(p(k+1)/p(k))-(p(k)-p(k-1))/log(p(k)/p(k-1))
    wgt0=-pres_a[0]+(pres_a[1]-pres_a[0])/log(pres_a[1]/pres_a[0])
    wgt1=pres_a[-1]-(pres_a[-2]-pres_a[-1])/log(pres_a[-2]/pres_a[-1])
    wgt=concatenate(([wgt0], sum_wgt))
    wgt=concatenate((wgt, [wgt1]))
    wgt=wgt/(pres_a[-1]-pres_a[0])
    #  print 'wgt', sum(wgt)
    # print wgt
    # print sum_wgt0
    
    # semilogy(wgt, pres_a)
    # show()
    
    return wgt



def get_total_column(gpf, gpname, use_vmr=True, molwgt=None):
    """ calculate the total column """
    gp=gpf.gpdict[gpname]
    axis_set=gpf.get_gp_attr(gpname, 'axis_set')
    ax_lon=axis_set[0]
    lon=ax_lon[:]
    nlon=size(lon)
    ax_lat=axis_set[1]
    lat=ax_lat[:]
    nlat=size(lat)
    ax_lz=axis_set[2]
    levels=ax_lz[:]
    levels=array(levels)
    levels=levels+1
    levels=levels.astype(int)
    print levels
    # pressure
    sp=gpf['PS']
    sp=array(sp)
    sp=squeeze(sp)
    gp_col=zeros(shape(sp), float)
    if (not use_vmr):
        conv_factor=100.0*molwgt/(gc.mg*gc.g0)  # the final unit could be kg/m2

    for ilon in range(nlon):
        for ilat in range(nlat):
            spres=sp[ilon, ilat]
            pres=pm.get_pres(spres, levels)
            pres=squeeze(pres)
            # print pres
            wgt=get_col_wgt(pres)
            prof=gp[ilon, ilat, :]
            gp_col[ilon, ilat]=sum(wgt*prof)
            if (not use_vmr):
                gp_col[ilon, ilat]=conv_factor*gp_col[ilon, ilat]
            
    print gp_col[3:6, 8]
    return gp_col

                
                    
                
 

    
    
        
        
    
    
    


            
    
                                 
    
    




