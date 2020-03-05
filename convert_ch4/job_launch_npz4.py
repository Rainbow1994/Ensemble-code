import bpnpz_em

def run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                        em_st, em_end, inpath, outpath):
    
    bpnpz_em.convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                           em_st, em_end, inpath, outpath)
    return 1



if (__name__=='__main__'):
    yyyy_st, month_st, nsteps=2010, 1, 4
    month_st=1
    month_end=12
    inpath='/home/lfeng/local_disk/lfeng/oco2_project/enkf_oco2_co2/enkf_output/'
    outpath='/home/lfeng/local_disk/lfeng/oco2_project/enkf_oco2_co2/enkf_output_nc/'
    
    select_part=4
    
    if (select_part==1):
        
        # job 1
        em_st, em_end=1, 77
    

    elif (select_part==2):
        
        # job 1
        em_st, em_end=77, 153
    

    elif (select_part==3):
        
        # job 1
        em_st, em_end=153, 229
    

    elif (select_part==4):
        
        # job 1
        em_st, em_end=229, 305
    else:
        em_st, em_end=305, 366
        
    run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                         em_st, em_end, inpath, outpath)
    
    
    
    
    
