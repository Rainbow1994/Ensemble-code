from numpy import *
import bpch2_rw_v2 as brw # need to handle the data
import gp_axis as gax
import gp_field as gf
import geo_constant as gc
import geos_chem_def as gcdf
import time_module as tm
import pres_mod_py as pm
import gen_plots as gpl
import read_cloud_map as rcm
# import scipy.weave as weave

def add_bpdata_to_gpf(bpdata, gpf, gpname=None):
    """ add gpdata into a data_collect """
    rlat=bpdata.grid.get_lat()
    rlon=bpdata.grid.get_lon()
    rz=bpdata.grid.get_z()
    ax_lon=gax.gp_axis('lon', rlon)
    ax_lat=gax.gp_axis('lat', rlat)
    ax_z=gax.gp_axis('level', rz)
    rdata=array(bpdata.data)
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
    
def add_map_to_gpf(grd_lon, grd_lat, grd_z, gpdata, gpname, gpf):
    """ add gpdata into a data_collect """
    ax_lon=gax.gp_axis('lon', grd_lon)
    ax_lat=gax.gp_axis('lat', grd_lat)
    ax_z=gax.gp_axis('level', grd_z)
    rdata=array(gpdata)
    sname=gpname
    
    sunit='PROB'
    gpf.add_gp(sname, rdata)
    gpf.set_gp_attr(sname, 'unit', sunit)
    gpf.set_gp_attr(sname, 'axis_set', [ax_lon, ax_lat, ax_z])
    
        
def get_ts_val(yyyy, mm, dd, \
               categorys=None, \
               tracers=None, \
               taus=None, \
               tranames=None,\
               dfile_prefix="ts.EN0001-EN0185",\
               as_gpf=True, \
               dpath=gcdf.data_path, \
               dfile_affix="bpch"):
    
    """ read the data into the one gp_field
    # we read in all the data
    """
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    full_flnm=gcdf.data_path+"/"+dfile_prefix.strip()+"."+sdate+"."+dfile_affix.strip()
    bpch2=brw.bpch2_file_rw(full_flnm, "r", do_read=1)

    if (bpch2.stat==0):
        ds=bpch2.get_data(categorys, tracers, None, None)

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
                ax_z=gax.gp_axis('level', ax_z)
                data_collect=gf.gp_field(full_flnm, axis_set=[ax_lon, ax_lat, ax_z])
                add_bpdata_to_gpf(bpdata, gpf)
            ngp=ngp+1
        bpch2=None
        return data_collect
    else:
        bpch2=None
        return ds

        
def setup_field(yyyy, mm, dd, em_st, em_end, datapath=gcdf.data_path, ctm_date0=None):
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)
    sem=r'EN%4.4d-EN%4.4d' % (em_st, em_end)
    full_flnm=datapath+"/"+"ts"+"."+sem+"."+sdate+".bpch"
    if (ctm_date0==None):
        ctmflnm=datapath+"/"+"ctm"+"."+sem+".bpch"
    else:
        ctmflnm=datapath+"/"+"ctm"+"."+sem+"."+ctm_date0+".bpch"
    
    ftraceinfo=datapath+"/"+"tracerinfo"+"."+sem+".dat"
    fdiaginfo=datapath+"/"+"diaginfo"+"."+sem+".dat"
    
    print 'Read tracer data from',   full_flnm
    # print ftraceinfo
    # print  fdiaginfo
    bpch2_ts=brw.bpch2_file_rw(full_flnm, "r", \
                               do_read=1,  ftracerinfo=ftraceinfo,\
                               fdiaginfo=fdiaginfo)
    print 'tracer number', bpch2_ts.ntracers
    #  bpch2_ts.print_datainfo()
    # get the total co
    categorys=None
    tracers=None
    tranames=['CO']
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
    gpf=gf.gp_field(sem, axis_set=[ax_lon, ax_lat, ax_z])
    iem=em_st
    for idata in range(len(data_list)):
        bpdata=data_list[idata]
        if bpdata==None:
            pass
        else:
            gpname=r'CO.%4.4d' % iem
            # gpname=r'CO.%4.4d' % bpdata.ntracer
            # print gpname
            add_bpdata_to_gpf(bpdata, gpf, gpname=gpname)
            iem=iem+1
    
            
    # get the total SURF
    categorys=None
    tracers=None
    tranames=['PS', 'AVGW', 'CF', 'CThgt', 'ODCOL']
    taus=None
    data_list, founded=bpch2_ts.get_data(categorys, tracers, taus, tranames)
    for bpdata in data_list:
        tn=bpdata.get_attr(['name'])
        gpname=tn[0].strip()
        
        add_bpdata_to_gpf(bpdata, gpf, gpname=gpname)

    # get the land-water and surface information
    print 'Read additional data LWI from ', ctmflnm
    
    utc=tm.time_array_to_utc(yyyy,mm, dd)
    # print utc
    # bpch2_ctm.print_datainfo()
        
    tau0=tm.utc_to_tai85(utc)
    tau0=tau0/(3600.0)

    ### this part is not necessary for CO
    founded=False
    if (found):
        
    
        bpch2_ctm=brw.bpch2_file_rw(ctmflnm, "r", do_read=2,\
                                    sel_categorys=['LANDMAP', 'TOTAOD'],sel_tracers=[1,1], sel_taus=[tau0, tau0])

    
        # print tau0
    
        # get the total SURF
        print 'tau0', tau0
        categorys=None
        tracers=None
        # tranames=['LWI']
        taus=[tau0]
        # taus=None
        data_list, founded=bpch2_ctm.get_data(categorys, tracers, taus, tranames)
        print founded
    
        bpdata=data_list[0]
        tau0, tau1=bpdata.get_attr(['tau0', 'tau1'])
        add_bpdata_to_gpf(bpdata, gpf, gpname='LWI')
        cld_lon, cld_lat, cld_z, cld_prob=rcm.read_cloud_map(mm)
        add_map_to_gpf(cld_lon, cld_lat, cld_z, cld_prob, 'CLDF', gpf)
        od_lon, od_lat, od_z, od_prob=rcm.read_od_map(mm)
        add_map_to_gpf(od_lon, od_lat, od_z, od_prob, 'ODP', gpf)
    return gpf
    


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

                
                    
                
 

    
if (__name__=="__main__"):
    from pylab import *
    gpf=setup_field(2003, 1, 1, 1, 8, datapath='/home/lfeng/local_disk_2/enkf_output/')
    # print gpf.gpdict.keys()
    lat=[0.0, -30]
    lon=[0.0, 90]
    xpos=[lon, lat, 0]
    
    # the second method,
    axis_set=gpf.get_gp_attr('CO.0001', 'axis_set')
    ax_lon=axis_set[0]
    ax_lat=axis_set[1]
    ax_lz=axis_set[2]
    
    lonp1, lonp2, lonwgt=ax_lon.getwgt(lon)
    latp1, latp2, latwgt=ax_lon.getwgt(lat)
    
    CO=gpf.gpdict['CO.0001']
    indx=range(size(latp1))
        
    prof1=latwgt[:, newaxis]*CO[lonp1[:], latp1[:], :]
    prof2=(1.0-latwgt[:, newaxis])*CO[lonp1[:], latp2[:], :]
    prof3=latwgt[:, newaxis]*CO[lonp2[:], latp1[:], :]
    prof4=(1.0-latwgt[:, newaxis])*CO[lonp2[:], latp2[:], :]
    co_prof=lonwgt[:, newaxis]*(prof1+prof2)+\
              (1.0-lonwgt[:, newaxis])*(prof3+prof4)
        
    gp=gpf['PS']

        
    prof1=latwgt[:]*gp[lonp1[:], latp1[:], 0]
    prof2=(1.0-latwgt[:])*gp[lonp1[:], latp2[:], 0]
    prof3=latwgt[:]*gp[lonp2[:], latp1[:], 0]
    prof4=(1.0-latwgt[:])*gp[lonp2[:], latp2[:], 0]

    prof=lonwgt[:]*(prof1+prof2)+\
              (1.0-lonwgt[:])*(prof3+prof4)
    
    sp=lonwgt[:]*(prof1+prof2)+\
              (1.0-lonwgt[:])*(prof3+prof4)
    levels=ax_lz[:]
    levels=array(levels)
    levels=levels+1
    levels=levels.astype(int)
    pres=pm.get_pres(sp, levels)
    
    # semilogy(1.0E9*co_prof[1,:], pres[1,:])
    # ylim([1000.0, 0.6])
    XCO=gpf.gpdict['CO.0004']
    dco=XCO-CO
    z=dco.flat
    z0=CO.flat
    ilvl=10
    coval=CO[:,:,ilvl]
    coval=1.0e9*coval
    decoval=dco[:,:,ilvl]
    decoval=1.0e9*decoval
    x3=gpf.gpdict['CO.0005']
    od_map=gpf['ODCOL']
    od_map=where(od_map<0.3, 1.0, 0.0)
    cld_map=gpf['CF']
    land_map=gpf['LWI']
    dco2=x3-CO
    decoval2=dco2[:,:,ilvl]
    decoval2=1.0e9*decoval2
    
    
    stitle='CO (pbm) at level 6 (EN0000) 20030101'
    subplot(3,1,1)
    rlon=array(ax_lon[:])
    rlat=array(ax_lat[:])
    
    
    gpl.plot_map(coval, rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    subplot(3,1,2)
    stitle='(EN0003-EN0000)'
    gpl.plot_map(decoval, rlon=rlon, rlat=rlat, use_pcolor=1, minv=-0.5, maxv=0.5, dv=0.1, cmap=cm.jet, title=stitle)
    subplot(3,1,3)
    stitle='(EN0004-EN0000)'
    gpl.plot_map(decoval2, rlon=rlon, rlat=rlat, use_pcolor=1, minv=-0.5, maxv=0.5, dv=0.1,cmap=cm.jet, title=stitle)
    
    savefig('co_fld.png')
    figure(2)
    col_co_1=get_total_column(gpf, gpname='CO.0001')
    col_co_1=1.0e9*col_co_1
    col_co_4=get_total_column(gpf, gpname='CO.0006')
    col_co_4=1.0e9*col_co_4
        
    subplot(3,1,1)
    rlon=array(ax_lon[:])
    rlat=array(ax_lat[:])
    stitle='(EN0001)'
    gpl.plot_map(col_co_1, rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    subplot(3,1,2)
    stitle='(EN0006)'
    gpl.plot_map(col_co_4, rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    subplot(3,1,3)
    stitle='(EN0004-EN0001)'
    gpl.plot_map(col_co_4-col_co_1, rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    
    figure(4)
    stitle='Cloud map'
    print shape(cld_map)
    subplot(2,1,1)
    gpl.plot_map(sum(cld_map[:,:,0:4], axis=2), rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    subplot(2,1,2)
    gpl.plot_map(od_map[:,:,0], rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    
    figure(5)
    stitle='Land Map'
    print shape(land_map)
    print land_map[0,:]
    
    subplot(2,1,1)
    gpl.plot_map(land_map[:,:,0], rlon=rlon, rlat=rlat, use_pcolor=1, cmap=cm.jet, title=stitle)
    savefig('land_map.ps')
    savefig('land_map.png')
    
    show()
    
    # print 'max-dev', max(z), max(z0)
    
    # show()
    
    
    
    # try to get the valf(self, gpname, xpos, xaxis=0, fill_val=None, threshold=0.0):ue at the location
    
    
        
        
    
    
    


            
    
                                 
    
    




