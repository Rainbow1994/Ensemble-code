import bpnc_em

def run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                        em_st, em_end, inpath, outpath):
    
    bpnc_em.convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                          em_st, em_end, inpath, outpath)
    return 1



if (__name__=='__main__'):
    yyyy_st, month_st, nsteps=2009, 1, 4
    month_st=1
    month_end=1
    inpath='/data/lfeng/esa_project/enkf_esa_co2/enkf_output/'
    outpath='/data/lfeng/esa_project/enkf_esa_co2/enkf_output_nc/'

    select_part=1
    
    if (select_part==1):
        
        # job 1
        em_st, em_end=1, 52
        
    # job2
    else:
        em_st, em_end=52, 102
    
    
    run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                         em_st, em_end, inpath, outpath)
    
    
    
    
    
