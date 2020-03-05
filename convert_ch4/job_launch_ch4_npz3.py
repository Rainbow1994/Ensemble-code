import bpnpz_ch4_em

def run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                        em_st, em_end, inpath, outpath):
    
    bpnpz_ch4_em.convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                           em_st, em_end, inpath, outpath)
    return 1



if (__name__=='__main__'):
    import sys
    yyyy_st, month_st, nsteps=2009,  1, 4
    month_st=1
    month_end=12
    
    inpath='../enkf_esa_ch4/enkf_output_years/enkf_output_'+str(yyyy_st)+'/'
    outpath='../enkf_esa_ch4/enkf_output_years/'+str(yyyy_st)+'/'
    select_part=int(sys.argv[1])
    if (select_part==1):
        
        # job 1
        em_st, em_end=1, 81
        
    # job2
    elif (select_part==2):        
        em_st, em_end=81, 161
    elif (select_part==3):
        em_st, em_end=161, 241
    elif (select_part==4):
        em_st, em_end=241, 321
    elif (select_part==5):
        em_st, em_end=321, 401
    elif (select_part==6):
        em_st, em_end=401, 481
    elif (select_part==7):
        em_st, em_end=481, 486
    
    
    
        
    
    run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                         em_st, em_end, inpath, outpath)
    
    
    
    
    
