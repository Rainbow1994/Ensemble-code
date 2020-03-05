import field_read as flr
import orbit_read as orr
import ak_read as akr
from pylab import *
from numpy import *
import time_module as tm
import pres_mod_py as pm
import gp_axis as gax
import obs_operator as obo
import netCDF_gen as nf
import numpy.random as rnd
import state_vector_step as stv_c
import etkf as et
import oco_feedback as ofb
import geos_chem_def as gcdf
from Scientific.IO.NetCDF import *

# if it is the not the first period, we only read in the ensemble 0 from the first fields
def data_collect(start_step, nst,
                 geos_datapath, \
                 obs_datapath,\
                 viewmode_list, \
                 not_first_period=False,\
                 err_scale=gcdf.err_scale, \
                 do_debug=False,\
                 do_dump=True, \
                 dumpflnm=None):
    """ doys  in date to be read in read in
    
    """
    
    fen=open(geos_datapath+'/'+'ens_pos.dat', 'r')
    line=fen.readline()
    line=fen.readline()
    terms=line.split()
    step=int(terms[1])
    nstep=int(terms[3])
    line=fen.readline()
    lines=fen.readlines()
    fen.close()
    em_st=list()
    em_end=list()
    yyyy_st=list()
    yyyy_end=list()
    doy_st=list()
    doy_end=list()
    co2flnm=list()
    sel_x_idx=range(1, 4)
    all_data=0
    
    for line in lines:
        line=line.strip()
        if (len(line)<1):
            break
    
        terms=line.split()
        print terms
        all_data=all_data+1
        em_st.append(int(terms[0]))
        em_end.append(int(terms[1]))
        yyyy_st.append(int(terms[2]))
        yyyy_end.append(int(terms[3]))
        doy_st.append(int(terms[4]))
        doy_end.append(int(terms[5]))
        co2flnm.append(terms[6])
    
            
    yyyy=yyyy_st[start_step]
    doy0=doy_st[start_step]
    doy1=doy0 +nst*step # 096 0406
    # set up the start days
    st_days=list()
    for iday in range(doy0, doy1+1, step):
        sday=r'%4.4dD%3.3d' % (yyyy, iday)
        st_days.append(sday)
        #        eday=r'%4.4dD%3.3d' % (yyyy, iday)
        
        
    print st_days

    do_debug=False
    iplot=0
    
    data_count=list()
    istep=0
    doys=arange(doy0, doy1)
    
    iday=0
    nusd_obs=0
    fclim=open('clim_co2.dat', 'r')
    lines=fclim.readlines()
    fclim.close()
    aprior=list()
    apr_pres=list()

    for iline in lines:
        terms=iline.split()
        aprior.append(float(terms[1]))
        apr_pres.append(float(terms[0]))

    aprior=array(aprior)
    apr_pres=array(apr_pres)
    apr_pres=log10(apr_pres)
    
    # starting to collect the observations and y
    #
    # figure(1)
    # show()
    # figure(1)
    sel_doys=[-1, -8, -15]
    int_step=0
    all_data_list=arange(all_data)
    int_step=0
    out_step=step
    data_count=list()
    print doy0, doy1, doys
    # tt=raw_input()
    day_cnt=0
    for doy in doys:
        yyyy, mm,dd=tm.doy_to_time_array(doy, yyyy)
        
        # if (day_cnt==0):
        # ctm_date0=r'%4.4d%2.2d%2.2d' % (yyyy, mm, dd)  
        
        print 'year mm dd', yyyy, mm, dd
        y=list()
        iend=0
        full_doy=r'%4.4dD%3.3d' % (yyyy, doy)
        sdate=r'%4.4dD%3.3d' % (yyyy, doy)
        # check whether it is necessary to include surface flux (stv) during cerntain days 
        iy=0
        if (int_step==0):
            dumpext=r"%2.2d" % nst
            dumpext="."+sdate+"_N"+dumpext
        
        viewmode=viewmode_list[doy-1]
        ncflnm_obs=obs_datapath+"/oco_"+viewmode+"."+sdate+".nc"
        print ncflnm_obs
        std_od, std_cflag=ofb.ncf_read(ncflnm_obs, ['od', 'cloud'])
        
        for eid in all_data_list:
            st_dd=doy_st[eid]
            end_dd=doy_end[eid]
            if (doy<st_dd):
                break
            
            if ((doy >=st_dd) and (doy <end_dd+step)):
                est=em_st[eid]
                eend=em_end[eid]
                sdate=r'%4.4dD%3.3d' % (yyyy, doy)
                ctm_date=st_dd
                print ctm_date
                ctm_yyyy, ctm_doy=yyyy, ctm_date
                ctm_yyyy, ctm_mm,ctm_dd=tm.doy_to_time_array(ctm_doy, ctm_yyyy)
                ctm_date0=r'%4.4d%2.2d%2.2d' % (ctm_yyyy, ctm_mm, ctm_dd)  
                
                ncflnm=obs_datapath+"oco"+"."+sdate+".nc"
                # print 'sel_eid', sel_eid
                obs=obo.obs_operator(yyyy, mm, dd, est, eend, \
                                     aprior=aprior, apr_pres=apr_pres, \
                                     viewmode=viewmode,\
                                     datapath=geos_datapath,\
                                     ctm_date0=ctm_date0)
                if (eid==0 and not_first_period):
                    ytop=est
                    
                else:
                    ytop=eend
                
                for em in range(est,ytop+1):
                    if (em==est):
                        obs.get_obs_prof(em, std_od=std_od, std_cf=std_cflag)
                    else:
                        # print 'iy', iy, em, est
                        obs.get_obs_prof(em, idx=used_idx, do_update=False)
                            
                    
                    if (iy==0):
                        # em_id is different from em. em_id is the 'real id' in the whole ensemble set 
                        em_id=obs.em_id[em-1]
                        print 'em_id', em_id, em-1
                        xgp0=obs.obs_xgp[em_id]
                        xgp=obs.obs_xgp[em_id]
                        print size(xgp), size(std_od), size(std_cflag)
                        obs_err=obs.obs_err
                        obs_err=array(obs_err)
                        obs_err=obs_err
                        # print 'shape obs+err', shape(obs_err)
                        rnd_obs_err=array(obs_err)
                        for iobs  in range(size(obs_err)):
                            err_val=obs_err[iobs]
                            rnd_err=rnd.normal(scale=err_val)
                            rnd_obs_err[iobs]=rnd_err
                            
                            # err_scale=1.0

                        if (do_debug):
                            subplot(2,1,1)
                            plot(obs_err)
                            plot(rnd_obs_err)
                            subplot(2,1,2)
                            hist(rnd_obs_err)
                            hist(obs_err)
                            show()
                
                
                        rnd_obs_err=err_scale*rnd_obs_err
                        cflag=obs.obs_cflag
                        otime=obs.obs_time
                        olat=obs.obs_lat
                        olon=obs.obs_lon
                        od=obs.obs_od
                        lwi=obs.obs_lwi
                        lwi=lwi.astype(int)
                        #                used_idx=where(logical_and(cflag==0, od<=0.3, lwi<>1))
                        osza=obs.obs_sza
                        sel1=logical_and(cflag==0, od<=0.3)
                        sel2=logical_and(lwi<>1, lwi<>2)
                        # used_idx=where(sel1)
                        # used_idx=where(logical_and(sel1, sel2))
                        # used_idx=where(cflag==0)
                        used_idx=where(logical_and(obs_err<4.0, sel1))
                        
                        used_idx=squeeze(used_idx)
                        print 'used_idx', len(used_idx)
                        xgp=xgp[used_idx]
                        xgp0=xgp0[used_idx]
                        
                        
                        obs_err=1.0e-6*obs_err[used_idx]
                        rnd_obs_err=1.0e-6*rnd_obs_err[used_idx]
                        imax=argmax(rnd_obs_err)
                        print 'max(obs err), max(rnd_obs_err)', 1.0e6*obs_err[imax], 1.0e6*rnd_obs_err[imax]
                        olat=olat[used_idx]
                        olon=olon[used_idx]
                        lwi=lwi[used_idx]
                        otime=otime[used_idx]
                        od=od[used_idx]
                        
                        # r=array(varData)
                        # r=r*r
                    else: # just others for ensemble 
                        em_id=obs.em_id[em-1]
                        # print 'em_id', em_id, em-1
                        xgp=obs.obs_xgp[em_id]
                        if (em==est):
                            print em,  est
                            print len(used_idx)
                            xgp=xgp[used_idx]
                            
                    if (istep>300):
                        print 'type xgp',type(xgp)
                        print 'len-xgp', len(xgp)
                
                
                    if (em==2):
                        print 'xgp', xgp[0:6]


                    y.append(array(xgp))

                    if (do_debug):
                        print ii, ne, shape(xgp)
                    if (do_debug and ii==4):
                        # figure(1)
                        # plot(xgp[0:300],'r')
                        # plot(xgp0[0:300], 'b')
                        z=xgp-xgp0
                        print 'max dev', max(z)
                    
                
                         
                    iy=iy+1
                    # show()
        y=array(y)
        y=transpose(y)
        print 'y-shape', shape(y), shape(xgp)
        
        if (istep>300):
            print type(y)
            print len(y)
            ix=y[0]
            print type(ix)
            
                # read in the data
        print ncflnm_obs
        obs_f=NetCDFFile(ncflnm_obs)
        yobs=obs_f.variables['xco2']
        yobs_err=obs_f.variables['err']
        yobs=array(yobs)
        # yobs_err=array(yobs_err)
        yobs_err=array(yobs_err)
        # print 'shape yobs', shape(yobs)
        yobs=squeeze(yobs)
        yobs_err=squeeze(yobs_err)
        
        obs_f.close()
        
        yobs=yobs[used_idx]
        yobs_err=yobs_err[used_idx]
    
        
        if (int_step==0):
            
            all_y=array(y)
            all_yobs=array(yobs)
            all_yobs_err=array(yobs_err)
            all_rnd_err=array(rnd_obs_err)
            all_lat=array(olat)
            all_lon=array(olon)
            all_lwi=array(lwi)
            all_time=array(otime)
            all_od=array(od)

            state_v=stv_c.state_vector(sdate, do_debug=False, datapath=geos_datapath)
            nx, ne=state_v.nx, state_v.ne
            
            print 'nx, ne', nx,ne
            nreg=(nx)/size(st_days)
            x=array(state_v.stv)
            
                                
        else:
            all_y=concatenate((all_y, y))
            all_yobs=concatenate((all_yobs, yobs))
            all_yobs_err=concatenate((all_yobs_err, yobs_err))
            all_rnd_err=concatenate((all_rnd_err, rnd_obs_err))
            all_lat=concatenate((all_lat, olat))
            all_lon=concatenate((all_lon, olon))
            all_lwi=concatenate((all_lwi, lwi))
            all_time=concatenate((all_time, otime))
            all_od=concatenate((all_od, od))
            
        print 'shape y & yobs', shape(y), shape(yobs)
        
        print 'istep & shape ',istep,  shape(all_y), shape(all_yobs), shape(all_yobs_err), shape(all_rnd_err)
        
        data_count.append(size(yobs))
            
        int_step=int_step+1
        print '*'*40+'int_step'+'*'*80
        print int_step
        
        if ((int_step==out_step) and do_dump):
            if (dumpflnm==None):
                ncdump=geos_datapath+'/'+'obs'+dumpext+"_"+sdate0+".nc"
            else:
                ncdump=geos_datapath+'/'+dumpflnm+"_"+dumpext+".nc"
            tmp_data_count=array(data_count)
            
            factor=1.0e6
            all_y=factor*all_y
            all_yobs=factor*all_yobs
            all_rnd_err=factor*all_rnd_err
            all_yobs_err=factor*all_yobs_err

            
            xnx=arange(nx)
            xne=arange(ne)
            xny=arange(size(all_y[:,0]))
            xney=arange(size(all_y[0,:]))
            dimTypes=['i', 'i','i','i', 'i']
            dimVars=[xnx, xne, xny, xney, doys]
            dimNames=['nx', 'ne', 'ny', 'ney', 'doys']
            x_info=ofb.geos_varinfo('x', 'f', ['nx', 'ne'], x)
            y_info=ofb.geos_varinfo('y', 'f', ['ny', 'ney'], all_y)
            yobs_info=ofb.geos_varinfo('obs', 'f', ['ny'], all_yobs)
            yobs_err_info=ofb.geos_varinfo('err', 'f', ['ny'], all_yobs_err)
            rnd_err_info=ofb.geos_varinfo('rnd_err', 'f', ['ny'], all_rnd_err)
            count_info=ofb.geos_varinfo('daily_count', 'i', ['doys'], tmp_data_count)
            lat_info=ofb.geos_varinfo('lat', 'f', ['ny'], all_lat)
            lon_info=ofb.geos_varinfo('lon', 'f', ['ny'], all_lon)
            time_info=ofb.geos_varinfo('time', 'f', ['ny'], all_time)
            od_info=ofb.geos_varinfo('od', 'f', ['ny'], all_od)
            lwi_info=ofb.geos_varinfo('lwi', 'i', ['ny'], all_lwi)
            ofb.ncf_write_by_varinfo(ncdump, dimNames, dimTypes, dimVars, \
                                     [x_info, y_info, yobs_info, yobs_err_info, \
                                      rnd_err_info, lat_info, lon_info, time_info, od_info, lwi_info, count_info])
            int_step=0
    

    data_count=array(data_count)
    print 'shape, all_y', shape(all_y)
    return x, all_y, all_yobs, all_yobs_err, all_rnd_err, data_count, doys, \
           all_lat, all_lon, all_time, all_lwi, all_od
        
    





def get_st_days(geos_datapath):
    fen=open(geos_datapath+'/'+'ens_pos.dat', 'r')
    line=fen.readline()
    line=fen.readline()
    terms=line.split()
    step=int(terms[1])
    nstep=int(terms[3])
    line=fen.readline()
    lines=fen.readlines()
    fen.close()
    em_st=list()
    em_end=list()
    yyyy_st=list()
    yyyy_end=list()
    doy_st=list()
    doy_end=list()
    co2flnm=list()
    for line in lines:
        line=line.strip()
        if (len(line)<1):
            break
    
        terms=line.split()
        # print terms
    
        em_st.append(int(terms[0]))
        em_end.append(int(terms[1]))
        yyyy_st.append(int(terms[2]))
        yyyy_end.append(int(terms[3]))
        doy_st.append(int(terms[4]))
        doy_end.append(int(terms[5]))
        co2flnm.append(terms[6])
    

    yyyy=yyyy_st[0]
    return step, nstep, yyyy_st, doy_st



