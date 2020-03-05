import bpch2_rw_py
flnm="/geos/u23/GC_DATA_/ctm/GEOS_1x1/GFED2_200601/2004/GFED2_C_200401.generic.1x1"
flnm_tmp='test_list.dat'
maxtracer=200
ios,title,tracer_id, lonres, latres,\
                     ix,jx,lx,\
                     ifirst, jfirst, lfirst,\
                     halfpolar, centre180, \
                     tau0,tau1,ntracers= \
                     bpch2_rw_py.read_bpch2_head(flnm,flnm_tmp, maxtracer)
print ntracers


