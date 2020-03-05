# default directories
import time_module as tm
run_path='/home/lfeng/local_disk_2/tagged_co2/sample_oco_run4_run5/'
data_path=run_path+'/enkf_output/' # the model output
obs_path=run_path+'/oco_obs/'            # observations
inv_path=run_path+'/oco_inv/'
def_input_file=run_path+'/input.geos' # GEOS-CHEM model input file
oco_orbit_path=run_path+'/gosat_orbit/' # OCO orbit 
oco_ak_path=run_path+'/gosat_ak/'       # OCO averaging kernel
#  starting time for geos chem simulation

st_yyyy, st_mm, st_dd=2006,1,5
st_doy=tm.day_of_year(st_yyyy, st_mm, st_dd)

# time resultion in day

temporal_resolution=8  #  the temporal resolution for inversions in days

# the ending time for geos chem simulation
# inversion lag window =temporal_resolution*n_inv_window
inv_lag_window=9 #

ntime_geos_chem=inv_lag_window # 2 *inv_lag_window if used the moving window # the last day of geos-chem simulation is given by ntime * temporal_resolution
inv_ntime=inv_lag_window

# spatial resolution

n_land_lat_div, n_land_lon_div=3,3
# n_ocean_lat_div,n_ocean_lon_div=3,3
n_ocean_lat_div,n_ocean_lon_div=2,2

region_num=11*n_land_lat_div*n_land_lon_div+11*n_ocean_lat_div*n_ocean_lon_div+1
num_used_en=max(340, region_num) # the restart file
output_daily_obs=True

new_restart=True
restart_file=data_path+'restart.jan2003.kalman.borealasia'  # 

#
# if choose do short will start a run with only 5 tagged tracers

view_type='new_aqua'
do_short= False
# view modes 
view_mode= 'glint'  # 'glint' # 'nadir', 'n16g16'

######  the following section  is  for inversion options ####
# observation options
do_update=True    # force the system to read in the data again
# if use old data provide the file name
xy_obs_file=data_path+'/'+view_mode+'_.2003D001_N02.nc'

select_obs=False  # use all observation 
add_rnd_err= False  # True # True # True
err_scale=1.0    

# model errors
model_land_err=2.5  # ppm
model_ocean_err=1.5 # ppm
model_err=1.0 # ppm

tcor_len=8.0


# tracer info file needs to initialize
def_tracerinfo_file=run_path+"tracerinfo.dat"
def_diaginfo_file=run_path+"diaginfo.dat"

#  a-priori error
#  rescale the error covariance.
# if necessary, you may use it to
# convert the default digonal error covariance to a more complicated one.
xnorm=1.0




# run control 
do_debug=False    
do_retry=False
do_init_run=True
maxne=inv_lag_window*region_num
start_step=0

# setting to read in the mop data
obs_version="L2V5.93.2.val"
obs_prefix="MOP02"







