import airs_ak_read as aak
import flib as flb
from numpy import *
import pres_mod_py as pm

def get_airs_convolve(rlon,rlat, sp, gp):
    # read in the class
    airs_ak=aak.average_kernal('ocean')
    
    nlon, nlat, nz=shape(gp)
    levels=arange(nz)
    levels=levels+1
    new_gp=zeros([nlon, nlat], float)
    
    for ilat in range(nlat):
        lat=rlat[ilat]
        rpos=[lat]
        ak_pres, ak_val=airs_ak.get_ak_prof(rpos)
        cur_sp=sp[:,ilat]
        prof_pres=pm.get_pres(cur_sp, levels)
        gp_prof=gp[:, ilat, :]
        prof_pres=-log10(prof_pres)
        
        ak_pres=-ak_pres
        ak_pres=ak_pres[::-1]
        ak_val=ak_val[::-1]
        # we have the same ak for the whole longitude, so we use half instead of        1d to get  vertical weight for each grid point
        
        #  the value out the actul pressure range is set to -999.0
                
        vpl, vpr, vwgt=flb.get_vertical_wgt_half(prof_pres, ak_pres)
        vpl=squeeze(vpl)
        vpr=squeeze(vpr)
        vwgt=squeeze(vwgt)
        # interpolate vertically
        # fill the value outside the actual pressure range with -999.0
                
        new_prof=flb.prof_vertical_intpl_1d(vpl, vpr, vwgt, gp_prof)
        # do the convolution using half (instead of 1d)
        
        
        convolve_val=flb.col_int_half(new_prof, ak_val)
        new_gp[:,ilat]=convolve_val[:]
    
        
    return new_gp
