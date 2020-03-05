from numpy import *
import os
flnm_tmp='stn_pos.temp'
fl_tmp=open(flnm_tmp, 'r')
lines_tmp=fl_tmp.readlines()
fl_tmp.close()
sel_yyyys=[2003, 2004,2005, 2006]
for yyyy in sel_yyyys:
    syyyy=str(yyyy)
    flnm="stn_pos_"+syyyy+".txt"
    fl=open(flnm, 'r')
    lines=fl.readlines()
    fl.close()
    iline=0
    nline=len(lines)
    flnm_tmp="stn_pos_"+syyyy+".temp"
    fl=open(flnm_tmp, 'w')
    print 'generate new stn_pos (obs usage)', flnm_tmp
    
    fl.write(lines[0])
    for iline in range(1, nline):
        line=lines[iline]
        line=line.replace('\n','')
        line=line.strip()
        line_tmp=lines_tmp[iline]
        line_tmp=line_tmp.replace('\n','')
        line_tmp==line_tmp.strip()
        new_line=line[0:-1]+' '+line_tmp[-1]
        # print line_tmp, '--', line_tmp[-1]
        # print line
        # print new_line
        fl.write(new_line+'\n')
    fl.close()


    os_cmd="mv "+flnm_tmp+" ./obs/"+flnm
    print os_cmd
    os.system(os_cmd)



    
