# default directories
import time_module as tm
en_path ='/scratch/local/shzhu/TEST_GC/TEST/2020_01_14_ensemble_run/'
run_path='./' #'/scratch/local/shzhu/TEST_GC/TEST/geosfp_4x5_tagCH4/'
temp_path = en_path+ 'temp/'
met_path = '/scratch/local/shzhu/GC_DATA/ctm/GEOS_4x5/GEOS_FP' #HEMCO_Config.rc
data_path = '/scratch/local/shzhu/GC_DATA/ctm' # input.geos
emis_path ='/exports/csce/datastore/geos/users/s2008420/' #path of emission datas 
res_path = en_path+ 'Restart_files/'
config_path = en_path+'Config_files/'
diagn_path = en_path+'Diagn_files'
mask_file = '/exports/csce/datastore/geos/users/s2008420/global_mask_20.nc'



#out_path=run_path+'enkf_output' # the model output
#obs_path=run_path+'/oco_obs/'            # observations
#inv_path=run_path+'/oco_inv/'
#def_input_file=run_path+'/input.geos' # GEOS-CHEM model input file
#oco_orbit_path=run_path+'/oco_orbit/' # OCO orbit 
#oco_ak_path=run_path+'/oco_ak/'       # OCO averaging kernel
##c/starting time for geos chem simulation

#st_yyyy, st_mm, st_dd=2008,11,1
st_yyyy, st_mm, st_dd = 2015,2,14
st_doy = tm.day_of_year(st_yyyy, st_mm, st_dd)

##c/time resultion in day

temporal_resolution=30
inv_lag_window=3
nstep=46
nstep_start=0

cfg_pb_file='./ens_ch4_cfg.2016'

##c/force the system to re-initialize to be a fixed value if True
new_restart= True # False
fixed_init_val=1.0e-8
restart_file = './GEOSChem.Restart.20160701_0000z.nc4'
rerun_now=True

rerun_date='20130101'
#ntracers = 40 
sub_sous = False
n_sous_loop  = 2
sub_tracers = True
n_tracer_loop = 1
#tracer_start = [1,11] #[1, maxtracer+1]
#tracer_end =[11,21] #[1, maxtracer+1]
#tracer_num = [10,10] 
tracer_start = [14]
tracer_end =[21]
tracer_num = [7]

##c selected run
select_runs=list(range(6, 7))
#select_sous=

#def_tracerinfo_file=run_path+"/tracerinfo.dat"
#def_diaginfo_file=run_path+"/diaginfo.dat"


# added by rainbow
n_regs = 20
n_sous = 2
sous_name = ['CH4_TAG_AN','CH4_TAG_NA']
## for HEMCO_Config.RC
emis_file_name = ['emi_anthro_s.nc','emi_nature_s.nc']
emis_var_name = ['Anthr' , 'Nature']
emis_time = ['2012/1/1/0','2015/1-12/1/0']
emis_unit = 'molec/cm2/s'
emis_rank = 'xy'