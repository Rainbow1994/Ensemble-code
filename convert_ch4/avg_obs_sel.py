import oco_feedback as ofb
from pylab import *
from numpy import *
import flib as flb
import reg_def as rgd
import time_module as tmdl


def get_daily_avg(yyyy, doy_list, lvl_st, lvl_end, doy_end=328, **keywords):
    # end of the assimilation period
    
    yyyy, mm,dd=tmdl.doy_to_time_array(doy_end, yyyy)
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, 11, 28)
    resflnm='co_flux.'+sdate
    tmp=['x','bm']
    xx, bend=ofb.ncf_read(resflnm+".nc", tmp)
    xx0=ones(size(xx), float)
    
    old_mm=0
    nreg=11
    inc_nx=12
    
    daily_obs=list()
    daily_prof=list()
    daily_prof0=list()
    daily_prof_sel=list()
    
    daily_cnt=list()
    # get hidx,  the location of tagged tracers in the reduced jacobian
    #  0== not used;  1-11 == FF+BF+BB at 11 regions;  12 == chemistry
    chm_idx=list()
    for doy in doy_list:
    
        yyyy, mm,dd=tmdl.doy_to_time_array(doy, yyyy)
        
        if (mm>old_mm):
            for imm in range(old_mm+1, mm+1):
                if (imm==1):
                    
                    hidx=[0]+range(1, nreg+1)+range(1,nreg+1)+[nreg+1]*5    
                    nx=12                
                    chm_idx.append(nx-1)
                    
                    new_hidx=[0]+range(nx+1, nx+inc_nx)+range(nx+1,nx+inc_nx)+[nx+inc_nx]*5
                    nx=nx+inc_nx
                    hidx=hidx+new_hidx
                    chm_idx.append(nx-1)
                    
                       
                else:
                    new_hidx=[0]+range(nx+1, nx+inc_nx)+range(nx+1,nx+inc_nx)+[nx+inc_nx]*5
                    nx=nx+inc_nx
                    hidx=hidx+new_hidx
                    chm_idx.append(nx-1)
                    
            old_mm=mm
        # print nx
        # print hidx
        print doy, yyyy, mm, dd, nx
        xx_sel=array(xx0)
        
        
        # required the model value 
        xx_list=list()
        key_words=list()
        do_it=0
        

        # prior vs posterior 
        if ('prior' in keywords):
            do_it=keywords['prior']
            
            
        if (do_it==1):
            xx_list.append(xx0)  # a-priori
            key_words.append('prior')
            
        do_it=0
        if ('posterior' in keywords):
            do_it=keywords['posterior']
            
        if (do_it==1):
            xx_list.append(xx)  # a-priori
            key_words.append('posterior')

        do_it=0

        # backgrounds
        
        if ('prior_bg' in keywords):
            do_it=keywords['prior_bg']
            
        if (do_it==1):
            xx_add=zeros(nx,float)
            xx_add[0:nreg]=xx0[0:nreg]
            key_words.append('prior_bg')
            xx_list.append(xx_add)
            
         
        
        if ('new_bg' in keywords):
            do_it=keywords['new_bg']

        if (do_it==1):
            xx_add=zeros(nx,float)
            xx_add[0:nreg]=xx[0:nreg]
            key_words.append('new_bg')
            xx_list.append(xx_add)
        
           
        # chemistry production
        
        if ('prior_chm' in keywords):
            do_it=keywords['prior_chm']
            
        if (do_it==1):
            xx_add=zeros(nx,float)
            xx_add[chm_idx]=xx0[chm_idx]
            xx_list.append(xx_add) 
            key_words.append('prior_chm')
        

        do_it=0
        if ('new_chm' in keywords):
            do_it=keywords['new_chm']

        if (do_it==1):
            xx_add=zeros(nx,float)
            xx_add[chm_idx]=xx[chm_idx]
            xx_list.append(xx_add)
            key_words.append('new_chm')
            

        do_it=0

        if ('prior_sel' in keywords):
            do_it=keywords['prior_sel']
            
        if (do_it>0):
            xx_add=zeros(nx,float)
            xx_add[do_it-1]=xx0[do_it-1]
            xx_list.append(xx_add)
            key_words.append('prior_sel')
        
        
        do_it=0

        if ('new_sel' in keywords):
            do_it=keywords['new_sel']
            
        if (do_it>0):
            xx_add=zeros(nx,float)
            xx_add[do_it-1]=xx[do_it-1]
            xx_list.append(xx_add)
            key_words.append('new_sel')
        
            

        
        cnt_avg, obs_avg, prof_avg, pres=\
                 get_daily_reg_avg(yyyy, mm, dd, xx_list,\
                                   hidx, nx, nreg, lvl_st, lvl_end)
                
        daily_obs.append(obs_avg)
        
        daily_prof.append(prof_avg)
        daily_cnt.append(cnt_avg)

    daily_obs=array(daily_obs)
    daily_prof=array(daily_prof)
    daily_cnt=array(daily_cnt)
    
    return daily_cnt, daily_obs, daily_prof, key_words, squeeze(pres)




def get_daily_reg_avg(yyyy, mm, dd, xx_list, hidx, nx, nreg, lvl_st, lvl_end):  
    """  calculate the daily average for regions  
    yyyy,mm, dd -------in------ year, month, day
    xx0, xx, -----in-------- the prior and posterior x values
    nx   -------in ---------- the number of x values
    hidx -----in --------   reduced from tagged regions to combined regions
    nreg ------in ---- regional number
    lvl_st, lvl_end-----  in the vertical range for averaging 
    
    cnt_avg ----- return ----- the number of obs in each region
    obs_avg, prof0_avg, prof_avg ----- return ------ the averaged observation, posterior profile,  and prior profile 
    
    """
    
    sdate=r'%4.4d%2.2d%2.2d' % (yyyy, mm,dd)

    matplotlib.rcParams['legend.fancybox'] = True

    # read obs
    resflnm='co_obs.'+sdate
    tmp=['lon', 'lat','pres', 'lvls', 'obs', 'ap_r', 'ak', 'err']
    olon, olat,opres, olvls, obs, oap_r, oak, oerr=ofb.ncf_read(resflnm+".nc", tmp)
    
    # read in  h
    
    
    nlvl=lvl_end-lvl_st+1
    
    obs_avg=zeros([nreg, nlvl], float)
    nmd=len(xx_list)
    prof_avg=zeros([nreg, nlvl, nmd], float)
    
    
    cnt_avg=zeros(nreg,integer)
    
    resflnm='co_k.'+sdate
    tmp=['h']
    
    prof_h=ofb.ncf_read(resflnm+".nc", tmp)
    # reduced to hm

 
    ridx=array(hidx)
    
    # print '11 region & month idx', hidx
    
    # print shape(prof_h)
    
    prof_h=squeeze(prof_h)
    
    hm = flb.reform_h(prof_h,olvls,ridx,nx)
    reg_id_list=rgd.get_region_id(olat, olon)
    

    # select the require region
    
    
    nobs=size(olon)
        
    for iobs in range(nobs):
        ml=olvls[iobs]
        ihm=hm[iobs, 0:ml,:]
        prof_obs=obs[iobs, :]-oap_r[iobs, :]
        ireg=reg_id_list[iobs]-1
        
        cnt_avg[ireg]=cnt_avg[ireg]+1
        obs_avg[ireg, 0:nlvl]=obs_avg[ireg, 0:nlvl]+prof_obs[lvl_st:lvl_end+1]
        imd=0 # model number 
        for xval in xx_list:
            prof=dot(ihm, xval[0:nx])
            prof_avg[ireg, 0:nlvl, imd]=prof_avg[ireg, 0:nlvl, imd]+prof[lvl_st:lvl_end+1]
            imd=imd+1
    
                
    for ireg in range(nreg):
        nobs=cnt_avg[ireg]
        if (nobs>0):
            obs_avg[ireg, 0:nlvl]=obs_avg[ireg, 0:nlvl]/nobs
            prof_avg[ireg, 0:nlvl, :]=prof_avg[ireg, 0:nlvl,:]/nobs
            
    return cnt_avg, obs_avg, prof_avg ,opres[0, lvl_st:lvl_end+1]


if (__name__=="__main__"):
    doy_st=1 # start date
    doy_end=30 # end date 
    yyyy=2006 # year 
    #selected verical range
    lvl_st=1  
    lvl_end=6
    sel_reg_idx=6
    
    # choose doys according to data availability
    
    usd_doy=list()

    fobs_list=open('./mop_obs_2006.list', 'r')
    raw_date_list=fobs_list.readlines()
    fobs_list.close()
    obs_date_list=list()
    for sobs_date in raw_date_list:
        sobs_date=sobs_date.replace('\n', '')
        sobs_date=sobs_date.strip()
        obs_date_list.append(sobs_date)

    
    doy_list=list()

    
    for doy in range(doy_st, doy_end):
        yyyy, mm,dd=tmdl.doy_to_time_array(doy, yyyy)
        sobs_date=r'%4.4d.%2.2d.%2.2d' % (yyyy, mm, dd)
        if (sobs_date in obs_date_list):
            # print sobs_date
            
            doy_list.append(doy)
    
        
        
    # get the daily regional observation/model average for doys in  doy_list
    # 
        
    daily_cnt, daily_obs, daily_prof, key_words, pres=\
               get_daily_avg(yyyy, doy_list, lvl_st, lvl_end, \
                             prior=1,\
                             posterior=1,\
                             prior_bg=1,\
                             new_bg=1,\
                             prior_chm=1,\
                             new_chm=1,\
                             prior_sel=sel_reg_idx,\
                             new_sel=sel_reg_idx)
    

    print shape(daily_prof)
    print key_words
    

    
    
    







