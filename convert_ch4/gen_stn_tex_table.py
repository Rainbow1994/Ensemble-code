from pylab import *
import gen_plots as gpl
import read_co2_flux as rco2_f
import compute_model_grid as cmgrd
import bpch2_rw_py as bpy
import read_stn_obs_year as robs_m
from numpy import *

cur_yyyy=2003

flnm_stn_list="stn_pos"+"_"+str(cur_yyyy)+".txt"
print flnm_stn_list

stn_c=robs_m.stn_obs(stn_list=flnm_stn_list, yyyy_st=cur_yyyy, yyyy_end=cur_yyyy)

nstn=len(stn_c.stn_name)
usd_stn=0
fl=open("stn.tex", "w")
for istn in range(nstn):
    if (stn_c.stn_use[istn]==1):
        line=r'%4.1f & %4.1f & %4d' % (stn_c.stn_lat[istn], stn_c.stn_lon[istn], int(1000*stn_c.stn_z[istn]))
        line=stn_c.stn_name[istn]+' & '+line+" \\\ "+'\n'
        fl.write(line) 
fl.close()


                     
