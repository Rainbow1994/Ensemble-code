#! /home/lfeng/epd/bin/python2.5
from pylab import *
import bpch2_rw_v2 as brw # need to handle the data
import gp_axis as gax   
import gp_field as gf
import geo_constant as gc
import geos_chem_def as gcdf # the data path etc 
import time_module as tmdl
import pres_mod_py as pm
import gen_plots as gpl
import read_cloud_map as rcm
import scipy.weave as weave
import field_read as frd
import read_mop_data as rmd
import read_mop_co_ap as rmca
import flib as flb
import moplib as mopl
import oco_feedback as ofb
import reg_def as rgd
import geo_constant as gc
import grid_py as gm
import co_emission as cosem
import co_jacobian as cojb
from numpy import *
import co_assim_step_v3 as coas

yyyy=2006

# start and end date

doy_st, doy_end=5, 335

# number of tagged chemistry production
nchm=1
nchem_type=5

# number of the tagged regional emission
nem_type=2
nreg=11

ntotal=1
#  tagged tracers
ntracer=ntotal+nem_type*nreg+nchm*nchem_type

# tagged background tracers 

nbg_reg=11  # the number of background  regions
nbg_chm=1  #  the number of the background chemistry

ntagged=0  # accumulated number of the  tagged tracers

#I

# construct list of hidx for the positions of the control variables in the Jacobian
# the number of tagged co sources & the corresponding control variables
# a) background

#  tagged tracer:  1 bg total + 22 bg regional emissions + 5 bg chemistry
#   x variables:    not used +     11 bg regions        +   1 bg chem
#
# b) monthly emission and chemistry production
#  tagged tracer:   1 total + 22 regional FF/BF/BB emissions  + 5 chemistry
#   x variables:     not used  +  11 regional emissions   +     1 chemistry


#  construct chem_pos for the tagged chemistry production in the full tagged sources
# a)  1 month
#   chem_pos=[28+23:28+28]
#   b)  2 month
#   chem_pos=[28+23:28+28]+[28+28+23:28+28+28]
#   the xx0 ------ the inital x values



hidx_list=list()
chem_pos_list=list()
nx_list=list()

hidx=list()
chem_pos=list()
chem_x_id=list()


nx=0
inc_nx=12

for imm in range(1, 13):
    if (imm==1):
        # background 
        reg_id=range(nx+1, nx+nreg+1)
        chem_id=[reg_id[-1]+1]
        hidx=[0]+reg_id*nem_type+chem_id*nchem_type
        nx=nx+inc_nx
        
    # other months
        
    reg_id=range(nx+1, nx+nreg+1)
    chem_id=[reg_id[-1]+1]
    new_hidx=[0]+reg_id*nem_type+chem_id*nchem_type
    
    chem_x_id.append(chem_id[0]-1)
    
    hidx=hidx+new_hidx
    nx=nx+inc_nx
    
    ntagged=len(hidx)
    chem_pos=chem_pos+range(ntagged-5, ntagged)
    
        
        
    hidx_list.append(hidx)
    chem_pos_list.append(chem_pos)
    nx_list.append(nx)
    print '-'*40+'month'+'-'*40
     
    # print nx
    # print hidx[0:56]
    # print chem_pos
    
    
#II

# construct intial xx0 & bb0 for the whole year
# note that  we only use the necessry parts of  xx0, bm0 and tm0
# for every month in the sequential inversion,
# although we construct the full matrix at this stage

# these arrays  can also be outputs from previous loops





xx0=ones(nx, float)
bm0=zeros([nx, nx], float)
tm0=identity(nx, float)


# regional emission and chemistry Production uncertainties


reg_err, chem_err=0.5, 0.01

for ix in range(nx):
    bm0[ix,ix]=reg_err
    
# assign errors to  chemistry production 
for ix in chem_x_id:
    print 'chem_x_id', ix
    bm0[ix, ix]=chem_err
    
# assign errors to background

bg_reg_err,  bg_chem_err=0.2, 0.001

for ix in range(nbg_reg):
    bm0[ix, ix]=bg_reg_err

bm0[nbg_reg, nbg_reg]=bg_chem_err


# model transport /chemistry error

mod_err=100.0 #  
# used vertical range  
pres_st=700.0
pres_end=350.0

# the  horizonal distance between two used observations
dlon, dlat=2.5, 2.0


print shape(xx0), shape(bm0), shape(tm0)

#III inversion by calling assim_mop_co in coas



coas.assim_mop_co(yyyy, doy_st, doy_end, \
                  xx0, bm0,tm0, \
                  nx_list,\
                  hidx_list, \
                  chem_pos_list, \
                  ntracer=ntracer,\
                  mod_err=mod_err,\
                  pres_st=pres_st,\
                  pres_end=pres_end,\
                  dlon=dlon,\
                  dlat=dlat)









