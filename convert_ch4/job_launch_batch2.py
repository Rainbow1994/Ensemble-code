import bpnpz_em

def run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                        em_st, em_end, inpath, outpath):
    
    bpnpz_em.convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                           em_st, em_end, inpath, outpath)
    return 1



if (__name__=='__main__'):
    import sys
    
    yyyy_st, month_st, nsteps=2011, 1, 4
    month_st=1
    month_end=12
    inpath='/data/lfeng/esa_project/enkf_esa_co2/enkf_output_2011/'
    outpath='/data/lfeng/esa_project/enkf_esa_co2/enkf_output_nc/'
    
   
    select_part=int(sys.argv[1])
    
    
    if (select_part==1):
        
        # job 1
        em_st, em_end=1, 52
    

    elif (select_part==2):
        
        # job 1
        em_st, em_end=52, 102
    
    run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                         em_st, em_end, inpath, outpath)
    
    
    
    
    
