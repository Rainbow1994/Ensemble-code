import os
fl=open('flnm_sel.lst')
lines=fl.readlines()
fl.close()
for line in lines:
    flnm=line.replace('\n', '')
    new_flnm=flnm.replace('SRON', 'UOL')
    cmd_line='cp '+flnm+' '+new_flnm
    print cmd_line
    os.system(cmd_line)

