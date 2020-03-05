#! /home/lfeng/ecmwf64/python2.5/bin/python2.5
import sys
from numpy import *
from pylab import *
import bpch2_rw_v2 as bpch2_mod
in_vals=sys.argv[1:]
inputs={}
for inval in in_vals:
    vname, vstr=inval.split("=")
    vname=str(vname.strip())
    vstr=str(vstr.strip())
    inputs.update({vname:vstr})

if ('file' in inputs):
    flnm=inputs['file']
else:
    while True:
        print 'give the name of bpch2 file'
        tt=raw_input()
        flnm=tt.strip()
        print flnm
        
        try:
            ftest=open(flnm, 'r')
            ftest.close()
            
        except IOError:
            print 'file '+flnm+'not found'
        
        print 'file exists'
        break

        


bpch2=bpch2_mod.bpch2_file_rw(flnm, 'r', do_read=1)

sel_tracer=-1

if ('tracer' in inputs):
    sel_tracer=inputs['tracer']

if (sel_tracer==-1):
    bpch2.print_datainfo()


            
    
