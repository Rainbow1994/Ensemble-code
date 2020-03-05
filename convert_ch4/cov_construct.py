from pylab import *
from numpy import *
import bpch2_rw_v2 as brw # need to handle the data
import gp_axis as gax
import gp_field as gf
import geo_constant as gc
import geos_chem_def as gcfs
import time_module as tm
import pres_mod_py as pm
import grid_py as gm
import gc_dist as gcd
import numpy.linalg as nlg
import gen_plots as gpl

def add_bpdata_to_gpf(bpdata, gpf, gpname=None):
    """ add gpdata into a data_collect """
    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
    ax_lon=gax.gp_axis('lon', rlon)
    ax_lat=gax.gp_axis('lat', rlat)
    ax_z=gax.gp_axis('level', rz)
    rdata=bpdata.data
    scat=bpdata.category
    stracer=r'%6.6d' % bpdata.ntracer
    
    if (gpname<>None):
        sname=gpname
    else:
        sname=bpdata.category.strip()+"/"+stracer
    
    sunit=bpdata.unit
    
    
    gpf.add_gp(sname, rdata)
    gpf.set_gp_attr(sname, 'unit', bpdata.unit)
    gpf.set_gp_attr(sname, 'axis_set', [ax_lon, ax_lat, ax_z])
    gpf.set_gp_attrs(sname, bpdata.attr)
    
        
def get_ts_val(yyyy, mm, dd, \
               categorys=None, \
               tracers=None, \
               taus=None, \
               tranames=None,\
               dfile_prefix="ts_satellite",\
               as_gpf=True, \
               dpath=gcfs.data_path, \
               dfile_affix="bpch"):
    
    """ read the data into the one gp_field
    # we read in all the data
    """
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    full_flnm=gcfs.data_path+"/"+dfile_prefix.strip()+"."+sdate+"."+dfile_affix.strip()
    bpch2=brw.bpch2_file_rw(full_flnm, "r", do_read=1)

    if (bpch2.stat==0):
        ds=bpch2.get_data(categorys, tracers, None, None)

    gpf.add_gp(sname, rdata)
    if (len(ds))==0:
        lds=list()
        lds.append(ds)

    ngp=0
    if (as_gpf):
        for bpdata in ds:
            # force delete 
            if (ngp==0):
                rlat=bpdata.grid.get_lat()
                rlon=bpdata.grid.get_lon()
                rz=bpdata.grid.get_z()
                ax_lon=gax.gp_axis('lon', rlon)
                ax_lat=gax.gp_axis('lat', rlat)
                ax_z=gax.gp_axis('level', rz)
                data_collect=gf.gp_field(full_flnm, axis_set=[ax_lon, ax_lat, ax_z])
                add_bpdata_to_gpf(bpdata, gpf)
            ngp=ngp+1
        bpch2=None
        return data_collect
    else:
        bpch2=None
        return ds

        
def setup_field(yyyy, mm, dd):
    
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    full_flnm=gcfs.data_path.strip()+"/"+"ts_satellite"+"."+sdate+".bpch"
    bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", do_read=1)
    # get the total co2
    categorys=None
    tracers=[1]
    tranames=['CO2']
    taus=None
    data_list=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    # bpch2_ts.print_datainfo()
    
    print founded, len(data_list)
    # set up gpfield 
    bpdata=data_list[0]
    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
    ax_lon=gax.gp_axis('lon', rlon)
    ax_lat=gax.gp_axis('lat', rlat)
    ax_z=gax.gp_axis('level', rz)
    gpf=gf.gp_field('CO2', axis_set=[ax_lon, ax_lat, ax_z])
    add_bpdata_to_gpf(bpdata, gpf, gpname='CO2')
    
    # get the total SURF
    categorys=None
    tracers=None
    tranames=['PS', 'AVGW', 'CF', 'CThgt']
    taus=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    for bpdata in data_list:
        tn=bpdata.get_attr(['name'])
        gpname=tn[0].strip()
        
        add_bpdata_to_gpf(bpdata, gpf, gpname=gpname)

    # get the land-water and surface information
    
    bpch2_ctm=brw.bpch2_file_rw('../ctm.bpch', "r", do_read=1)
    utc=tm.time_array_to_utc(yyyy,mm, dd)
    # print utc
    # bpch2_ctm.print_datainfo()
        
    tau0=tm.utc_to_tai85(utc)
    tau0=tau0/(3600.0)
    # print tau0
    
    # get the total SURF
    categorys=None
    tracers=None
    tranames=['LWI']
    taus=[tau0]
    # taus=None
    data_list, founded=bpch2_ctm.get_data(categorys, tracers, taus, tranames)
    bpdata=data_list[0]
    tau0, tau1=bpdata.get_attr(['tau0', 'tau1'])
    add_bpdata_to_gpf(bpdata, gpf, gpname='LWI')
    
    return gpf

    
if (__name__=="__main__"):
    
    # from pylab import *
    
    gpf=setup_field(2003, 1, 10)
    print gpf.gpdict.keys()
    axis_set=gpf.get_gp_attr('CO2', 'axis_set')
    ax_lon=axis_set[0]
    ax_lat=axis_set[1]
    ax_lz=axis_set[2]
    rlon=array(ax_lon[:])
    rlat=array(ax_lat[:])
    
    
    CO2=gpf.gpdict['CO2']
    lwi=gpf.gpdict['LWI']
    gp=gpf.gpdict['PS']

    print size(rlon)
    print size(rlat)

    gm.grid_mod.compute_grid()
    nx=gm.grid_mod.get_x_size()

    if (size(rlon)<>nx):
        print 'size error ',nx, size(rlon)
    

    idx=arange(1,nx+1)
    lon_g=gm.grid_mod.get_xmids(idx)
    lon_g=array(lon_g)
    
    ny=gm.grid_mod.get_y_size()
    if (size(rlat)<>ny):
        print 'size error ',ny, size(rlat)
    
    idy=arange(1,ny+1)
    
    lat_g=gm.grid_mod.get_ymids(idy)
    lat_g=array(lat_g)
    sf_area=gm.grid_mod.get_areas(idx,idy)
    
    #  print rlat[:]
    # print lat_g[:]
    
    lon_m, lat_m=meshgrid(lon_g, lat_g)
    lon_m=transpose(lon_m)
    lat_m=transpose(lat_m)
    print shape(lon_m)
    print lon_m[3,5], lat_m[3,5], lon_g[3], lat_g[5]
    
    print shape(lat_m)
    lon_m=reshape(lon_m, [-1,1])
    lat_m=reshape(lat_m, [-1,1])
    lon_m=squeeze(lon_m)
    lat_m=squeeze(lat_m)
    sf_area=reshape(sf_area, [-1,1])
    sf_area=squeeze(sf_area)
    dist=gcd.get_circle_distance(lon_m, lat_m)
    lwi=lwi[:,:,0]
    lwi_m=reshape(lwi, [-1,1])
    lwi_m=squeeze(lwi_m)
    sf_err=zeros(shape(lwi_m), float)
    print shape(sf_err)
    err_land=1.0e-16 # [kgC/m2/s]^2
    err_ice=err_land #assume
    err_w=1.0E-18  #   [kgC/m2/s]^2
    land_a=where(lwi_m==0)
    sf_err[land_a]=err_land
    
    w_a=where(lwi_m==1)
    sf_err[w_a]=err_w
    
    ice_a=where(lwi_m==2)
    sf_err[ice_a]=err_land
    sf_err=sf_err*sf_area*sf_area*3600*3600*(44.0/12)**2 # convert to [KgCO2/hour]^2
    cor_len=array([900.0, 2000.0, 900.0])
    conv=gcd.gen_conv(cor_len, lwi_m, sf_err, dist)
    u,w,v=nlg.svd(conv)
    # reconstuct the error covariance
    sel_n=1000
    sel_u=u[:,0:sel_n]
    sel_w=w[0:sel_n]
    sel_v=v[0:sel_n,:]
    sel_u=sel_u*sqrt(sel_w)
    sel_v=transpose(sel_v)*sqrt(sel_w)
    sel_v=transpose(sel_v)
    re_conv=dot(sel_u, sel_v)
    
    figure(1)
    subplot(2,1,1)
    imshow(conv)
    subplot(2,1,2)
    imshow(re_conv)
    figure(2)
    semilogy(arange(size(w)),w)
    figure(3)
    plot(re_conv[80, :],'b')
    plot(conv[80,:],'r')
    
    plot(re_conv[180, :],'g:')
    plot(conv[180,:],'k:')
    legend(['80', '80_s', '180', '180_s'])
    xlim([0, 500])
    figure(4)
    sel_data=conv[:,1600]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,1,1)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,1,2)
    sel_data=re_conv[:,1600]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    figure(5)
    sel_data=u[:,0]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,1)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,2)
    sel_data=u[:,1]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    sel_data=u[:,2]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,3)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,4)
    sel_data=u[:,3]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    figure(6)
    sel_data=u[:,4]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,1)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,2)
    sel_data=u[:,5]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    sel_data=u[:,6]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,3)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,4)
    sel_data=u[:,7]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    figure(7)
    sel_data=u[:,28]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,1)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,2)
    sel_data=u[:,29]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    sel_data=u[:,30]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,3)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,4)
    sel_data=u[:,31]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    figure(8)
    sel_data=u[:,32]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,1)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,2)
    sel_data=u[:,33]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    sel_data=u[:,34]
    sel_data=reshape(sel_data, [nx, ny])
    subplot(2,2,3)
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)
    subplot(2,2,4)
    sel_data=u[:,35]
    sel_data=reshape(sel_data, [nx, ny])
    gpl.plot_map(sel_data, lon_g, lat_g, use_pcolor=1)

    
    show()
    
    
    
    
    
    
    
    
    
    # try to get the valf(self, gpname, xpos, xaxis=0, fill_val=None, threshold=0.0):ue at the location
    
    
        
        
    
    
    


            
    
                                 
    
    




