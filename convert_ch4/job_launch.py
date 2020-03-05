import pp
import bpnc_em

def run_bpch_convert(yyyy_st, month_st, month_end, nsteps, \
                        em_st, em_end, inpath, outpath):
    
    bpnc_em.convert_em_file_to_netcdf(yyyy_st, month_st, month_end, nsteps, \
                                          em_st, em_end, inpath, outpath)
    return 1



if (__name__=='__main__'):
    ppservers = ()
    job_server = pp.Server(ncpus=2, ppservers=ppservers)
    print "Starting pp with", job_server.get_ncpus(), "workers"
    yyyy_st, month_st, nsteps=2011, 1, 5
    month_st=12
    month_end=12
    
    inpath='/scratch/local/bkup_keeling/enkf_output_144/2011/'
    outpath='/scratch/local/bkup_keeling/enkf_output_nc/2011/'
    
    # job 1
    em_st, em_end=1, 81
    
    job1 = job_server.submit(run_bpch_convert, (yyyy_st, month_st, month_end, nsteps, \
                                                   em_st, em_end, inpath, outpath), modules=('bpnc_em',), group='decnc')
    
    # job2
    
    em_st2, em_end2=81, 146
    job2 = job_server.submit(run_bpch_convert, (yyyy_st, month_st, month_end, nsteps, \
                                                   em_st2, em_end2, inpath, \
                                                   outpath), modules=('bpnc_em',), group='decnc')
    
    
    
    result1=job1()
    result2=job2()
    
    
    
    
