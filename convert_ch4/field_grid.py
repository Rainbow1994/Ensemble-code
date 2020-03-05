""" this module is used to regrid data to the given h/v resolution """

from pylab import *
# from matplotlib.toolkits.basemap import Basemap, shiftgrid

try: 
    from matplotlib.toolkits.basemap import Basemap, shiftgrid
except ImportError:
    from mpl_toolkits.basemap import Basemap, shiftgrid

from numpy import *

import time_module as tm
import gp_axis as gax
import flib
import oco_feedback as ofb
import pres_mod_py as pm
import grid_py as gm
import bpch2_rw_v2 as brw

def get_model_grid(return_edge=False):
    #  # print'get_grid'
    gm.grid_mod.compute_grid()
    # # print'try setup grid'
    IIPAR=gm.grid_mod.get_x_size()
    JJPAR=gm.grid_mod.get_y_size()

    JY=arange(1, JJPAR+1)
    YY = gm.grid_mod.get_ymids( JY )
    IX=arange(1, IIPAR+1)
    XX = gm.grid_mod.get_xmids( IX )
    sf_area=1.0E4*gm.grid_mod.get_areas(IX, JY)
    
    IX=arange(1, IIPAR+2)
    Iy=arange(1, JJPAR+2)
    xedge=gm.grid_mod.get_xedges(IX)
    yedge=gm.grid_mod.get_yedges(JY)
    if (return_edge):
        return XX, YY, xedge, yedge, sf_area
    else:
        return XX, YY

def get_lsce_grid_area(lon, lat,dlon=3.75, dlat=2.5):
    Re=  6.375e6
    # irregular at the 
    nlat=size(lat)
    lat_edges=zeros(nlat+1, float)
    lat_edges[0]=-90.0
    for ilat in range(1, nlat-1):
        lat_edges[ilat]=lat[ilat]-0.5*dlat
    
    lat_edges[nlat-1]=lat[nlat-1]+0.5*dlat
    lat_edges[nlat]=90.0
    
    
    lat_areas=zeros(nlat, float)
    
    ns=size(lat_areas)
    idx_ns=arange(ns)
    lat_edges=(pi/180)*lat_edges
    sin_ed=sin(lat_edges)
    
    lat_areas[idx_ns]=Re*Re*(sin_ed[idx_ns+1]-sin_ed[idx_ns])
    
    
    
    # new_lon
    
    
    nlon=size(lon)
    lon_edges=zeros(nlon+1, float)
    lon_edges[0]=-180.0

    # as 180 is included, here is nlon instead of nlon-1
    
    for ilon in range(1, nlon):
        lon_edges[ilon]=lon[ilon]-0.5*dlon
    
    lon_edges[nlon]=180.0
    
    lon_edges=(pi/180)*lon_edges
    areas=zeros([nlon, nlat], float)
    
    nx, ny=shape(areas)
    idx=arange(nx)
    
    for ilat in range(nlat):
        areas[idx, ilat]=lat_areas[ilat]*(lon_edges[idx+1]-lon_edges[idx])
    
    return areas
    
    
    
def get_model_pressure(lx, mod_type=5, ps=None, psfile=None, cater_ps='PS',
                       tracer_ps=None, tau_ps=None):
    
    """
    ps :  ---in ---:  array of (nlon, nlat) surface pressure
    """

    if (psfile<>None):
        # read from geos pressure file
        if ('.nc' in psfile): # the netcdf file
            varnames=['longitude', 'latitude', 'p']
            grd_lon, grd_lat, ps=ofb.ncf_read(psfile, varnames)
            ps=ps[:,:,0]
            ps=squeeze(ps)
            
        else:
            # grd_lon, grd_lat=get_model_grid()
            
            catergory_out,tracer_out,unit_out,\
                                               tau0_out,out_array= \
                                               get_model_value(psfile, catergory=cater_ps, tracer=tracer_ps, tau0=tau_ps)
            print 'unit for ps', unit_out.strip()
            
            ps=squeeze(out_array)
            print 'shape of ps, min(ps), max(ps)', shape(ps), min(ps.flat), max(ps.flat)
            
    
    
    levels=arange(lx)
    levels=levels+1
    
    if (mod_type==4):  # GEOS-4
        if (lx==30):
            use_reduced=1
        else:                 
            use_reduced=0
    else:                    # GEOS-5
        if (lx<50):
            use_reduced=1
        else:
            use_reduced=0
            # 
    pres = pm.get_pres_mod_2d(ps,levels,mod_type,use_reduced)
    print shape(pres), shape(ps)
    
    
    return pres

def get_model_pressure_edge(ps, mod_type=5, use_reduced=1):
    
    """
    ps :  ---in ---:  array of (nlon, nlat) surface pressure
    """

    if (mod_type==5):
        lx=71
        if (use_reduced==1):
            lx=47
    else:
        lx=71
        if (use_reduced==1):
            lx=31
    
    
    levels=arange(lx+1)
    levels=levels+1
    
    pres = pm.get_pres_edge_mod_2d(ps,levels,mod_type,use_reduced)
    
    print shape(pres), shape(ps)
    
    
    return pres

def get_mod_height(pres_edge, t):
    bxheight, alt=pm.get_bxheight(pres_edge, t)
    return bxheight, alt









def get_model_value(filename, catergory=None, tracer=None, tau0=None):
    """ this is wrapper for read in data """

    import bpch2_rw_py as bp
    
    
    if (catergory==None):
        catergory_in='NONE'
    else:
        catergory_in=catergory.strip()
        
    if (tracer==None):
        tracer_in=-999
    else:
        tracer_in=tracer
        
    if (tau0==None):
        tau0_in=-999.0
    else:
        tau0_in=tau0
    
        
    catergory_out,tracer_out,unit_out,\
                                       tau0_out,ix,jx,lx,out_array,stat = \
                                       bp.read_bpch2_firstmatch(filename.strip(),catergory_in,tracer_in,tau0_in)

    if (stat <> 0):
        print 'error in reading '+flnm, state
        return none
    

    out_array=out_array[0:ix, 0:jx, 0:lx]
    
    return catergory_out,tracer_out,unit_out,\
           tau0_out,out_array


def regrid_data(data, lon, lat, \
                new_lon, new_lat, \
                pressure=None, new_pres=None):
    
    """ write data into one open bpch2 file 
    Arguments:
    data: ---in----: array of (nlon, nlat, nz), 3D-geos field
    lon: ---in ---:  array of (nlon) longitude
    lat: ---in ---:  array of (nlat) latitude
    pressure:  ---in ---:  array of (nlon, nlat, nz) pressure at each model level
    new_pres:  ---in ---:  array of (nlon, nlat, nz) pressure at each model level
    new_lon, new_lat, new_pres: ---in---- : array of (new_nlon, new_nlat, new_lz)
        
    
    
    """
    
    
    
    ax_lat=gax.gp_axis('lat', lat)
    ax_lon=gax.gp_axis('lat', lon)

    lonp1, lonp2, lonw=ax_lon.getwgt(new_lon)
    latp1, latp2, latw=ax_lat.getwgt(new_lat)
    
    var_dims=shape(data)
    ndims=size(var_dims)
    
    if (ndims==2):
        new_data1=lonw[:,newaxis]*data[lonp1, :]+(1.0-lonw[:,newaxis])*data[lonp2,:]
        new_data=latw[newaxis, :]*new_data1[:,latp1]+(1.0-latw[newaxis, :])*new_data1[:,latp2]
    elif (ndims==3):
        new_data1=lonw[:,newaxis, newaxis]*data[lonp1, :, :]+(1.0-lonw[:,newaxis, newaxis])*data[lonp2,:,:]
        new_data=latw[newaxis, :, newaxis]*new_data1[:,latp1, :]+(1.0-latw[newaxis, :, newaxis])*new_data1[:,latp2, :]
    
    # print 'new_z in regrid,old_mod, new_ond', size(new_z), old_mod, new_mod
    
    # do vertical interpolation if required 
    if ((new_pres<>None) and (pressure<>None)):
    
        old_pres1=lonw[:,newaxis, newaxis]*pressure[lonp1, :, :]+(1.0-lonw[:,newaxis, newaxis])*pressure[lonp2,:,:]
        old_pres=latw[newaxis, :, newaxis]*old_pres1[:,latp1, :]+(1.0-latw[newaxis, :, newaxis])*old_pres1[:,latp2, :]

        print 'old_pres', shape(old_pres)
        org_lon, org_lat, org_lz=shape(new_data)
        sel_lat=30.0
        sel_lon=63.0
        ilat=argmin(abs(new_lat-sel_lat))
        ilon=argmin(abs(new_lon-sel_lon))
        
        old_pres=squeeze(old_pres)
        new_data=squeeze(new_data)
        
        semilogy(new_data[org_lon/2, org_lat/2,:], old_pres[org_lon/2, org_lat/2,:], 'g')
        semilogy(new_data[ilon, ilat,:], old_pres[ilon, ilat,:], 'g--')
        semilogy(new_data[30, 20,:], old_pres[30, 20,:], 'k--')
        
        old_pres_log=-log10(old_pres)
        print old_pres_log[30,20,:]
        
        new_pres_log=-log10(new_pres)
        print new_pres_log[30,20,:]
        
        pl, pr,wgt=flib.get_vertical_wgt_2d(old_pres_log,new_pres_log)
        print shape(pl), shape(pr), shape(wgt)
        print pl[30, 20, 10], pr[30, 20, 10], wgt[30, 20, 10]
        print old_pres_log[30, 20,  pl[30, 20, 10]],  old_pres_log[30, 20,  pr[30, 20, 10]], \
              new_pres_log[30, 20, 10]
        
        prof=new_data
        out_prof = flib.prof_vertical_intpl_2d(pl,pr,wgt,prof)
        semilogy(out_prof[30, 20,:], new_pres[30, 20,:], 'k')
        new_data=array(out_prof)
        
    return new_data
    
            
                    # read in the pressure mode
                    
        
def get_model_zonal_mean(data, pressure, pres_lvl):
    print '----in get_model_zonal_mean-----'
    print 'shape(data), shape(pressure), shape(pres_lvl)',  shape(data), shape(pressure), shape(pres_lvl)
    
    vals=flib.get_zonal_mean(data, pressure, pres_lvl)

    print 'shape vals', shape(vals)
    print 'vals[30,0], [30, 10]', vals[30, 0], vals[30, 10]
    print '----leave get_model_zonal_mean-----'
    
    return vals

if (__name__=='__main__'):
    psfile="/geos/u23/enkf_std/enkf_output_22/ts.EN0117-EN0139.20030319.bpch"
    lx=30
    
    pressure=get_model_pressure(lx, mod_type=4, ps=None, psfile=psfile, \
                                cater_ps='TIME-SER',  \
                                tracer_ps=15, tau_ps=None)
    print shape(pressure)
    
def get_model_colum(data, pressure):
    print '----in get_model_column-----'
    print 'shape(data), shape(pressure)',  shape(data), shape(pressure)
    
    colwgt=flib.get_col_wgt_2d(pressure)
    colval=flib.col_int_2d(data, colwgt)
    print 'shape vals', shape(colval)
    print '----leave get_model_column-----'
    
    return colval

def load_ts_field(bpchflnm, ftracerinfo, fdiaginfo):
    # print ftraceinfo
    # print  fdiaginfo
    bpch2_ts=brw.bpch2_file_rw(bpchflnm, "r", \
                               do_read=1,  ftracerinfo=ftracerinfo,\
                               fdiaginfo=fdiaginfo)
    return bpch2_ts



if (__name__=='__main__'):
    psfile="/geos/u23/enkf_std/enkf_output_22/ts.EN0117-EN0139.20030319.bpch"
    lx=30
    
    pressure=get_model_pressure(lx, mod_type=4, ps=None, psfile=psfile, \
                                cater_ps='TIME-SER',  \
                                tracer_ps=15, tau_ps=None)

    print shape(pressure)
    
    catergory_in=None
    tracer_in=1
    tau0_in=None
    
    catergory_out,tracer_out,unit_out,\
                                       tau0_out,out_array= \
                                       get_model_value(psfile, catergory=catergory_in, tracer=tracer_in, tau0=tau0_in)

    
    print catergory_out.strip(), tracer_out, tau0_out
    
    
    data=squeeze(out_array)
    colval=get_model_colum(data, pressure)
    print 'colval:shape, min, max', shape(colval), min(colval.flat), max(colval.flat)
    
    
    
        
        
