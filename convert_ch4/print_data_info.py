#! /home/lfeng/tmp_cp/ecmwf/python2.5/bin/python2.5
import geos_chem_def as gcdf
import sys

from bpch2_rw_v2 import *
if (len(sys.argv)>1):
    flnm=sys.argv[1]
    if ('/' in flnm):
        flnm=flnm.strip()
    else:
        flnm=gcdf.data_path+flnm.strip()

else:
    flnm=gcdf.data_path+'ts.EN0001-EN0185.20030129.bpch'
flnm=flnm.strip()
# print flnm

bpch2=bpch2_file_rw(flnm, 'r', do_read=0)
print '='*5+flnm+'='*5
print '*'*60
bpch2.print_datainfo()


