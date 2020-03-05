#! /home/lfeng/ecmwf64/python2.5/bin/python2.5
import input_geos_gen as igg
import co2_emission as co2em
import sys
import os
import restart_gen as rg
import time_module as tm
import time as systime
import geos_chem_def as gcdf
print '*'*80
print ''*30+'CO2 ENSEMBLE RUN DRIVER'+'*'*30
print '*'*80
print ' '*30

print '======>Step 1: Generate co2 emission data<======'

# starting time 

yyyy=2006
mm=1
dd=1
doy0=1
temp_res=8 # 8 days 
timestep=temp_res*24.0*3600.0 #  8-days
ntime=12
doy1=doy0+ntime*temp_res-1
pos=list()
ipos=0
gmt=systime.gmtime()
a_mst=[1, 186, 370]
a_mend=[185, 369, 553]
# a_mst=[1]
# a_mend=[185]
nrun=len(a_mst)
# ftt=open(gcdf.data_path+'/'+"ens_pos.dat", "w")
ftt=open('./'+"ens_pos.dat", "w")

line='geos_chem run at %4.4d%2.2d%2.2d, %2.2d:%2.2d:%2.2d' % (gmt[0], gmt[1], gmt[2], gmt[3], gmt[4], gmt[5])
print line
ftt.write(line+'\n')
line=r'temp_res: %4.4d  nstep: %4.4d' % (temp_res, ntime)
ftt.write(line+'\n')
line='mem_st mem_end year_st  year_end day_st day_end flnm'
ftt.write(line+'\n')
for irun in range(nrun):
    mst=a_mst[irun]
    mend=a_mend[irun]
    line=r'%4.4d %4.4d %4.4d %3.3d %3.3d %3.3d' % (mst, mend, yyyy, yyyy,doy0, doy1)
    line=line+ ' '+'CO2EMISSION'
    print line
    ftt.write(line+'\n')
ftt.close()
