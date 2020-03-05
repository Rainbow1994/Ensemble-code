from numpy import *
import standard_atmosphere as stam
import time_module as tm
import read_lsce_air as rlsce
import read_contrail_air as rcont

def gen_planeflight_headlines(user='Liang Feng', sdate='08 Jun 2009'):
    headlines=['Planeflight.dat',\
               user, \
               sdate]
    return headlines

def gen_planeflight_midlines():
    lines=['-------------------------------------------------------------------------------',\
           'Now give the times and locations of the flight',\
           '-------------------------------------------------------------------------------', \
           'Point Type  DD-MM-YYYY HH:MM   LAT    LON    PRESS   VMR'\
           ]

    return lines
def gen_planefight_endline():
    line='99999 END   0- 0- 0    0 :0    0.00   0.00   0.00   0.00'
    return line


def gen_planeflight_sep_line():
    line='-------------------------------------------------------------------------------'
    return line

def gen_planeflight_tracer_line(tracer_list):
    """ define which tracer will be written out """
    line_list=list()
    for itr in tracer_list:
        sline=r'TRA_%3.3d' % itr
        line_list.append(sline)
    return line_list

def gen_planeflight_met_line(met_list):
    """ define which tracer will be written out """
    line_list=list()
    for smet in met_list:
        smet=smet.strip()
        if (smet=='PSURF'):
            sline='GMAO_PSFC'
        elif (smet=='TEMP'):
            sline='GMAO_TEMP'
        elif (smet=='U'):
            sline='GMAO_UWND'
        elif (smet=='V'):
            sline='GMAO_VWND'
        else:
            sline='GMAO_'+smet
        
        line_list.append(sline)
        
    return line_list


if (__name__=='__main__'):
    
    record_list=list()
    
    sel_year=2003
    # read the contrail data
    flnm='./air_obs/contrail.dat'
    
    record_list=rcont.read_contrail_flight_info(flnm, sel_year, record_list=record_list)
    print 'found contrail records:', len(record_list)
    
    fl_list=['./air_obs/HNG_XXXX_ext.co2', './air_obs/GRI_XXXX_ext.co2',\
             './air_obs/ORL_XXXX_ext.co2', './air_obs/FTL_XXXX_ext.co2']

    # read lsce data
    
    for flnm in fl_list:
        record_list=rlsce.read_lsce_flight_info(flnm, sel_year, record_list=record_list)
        
    print 'found total records:', len(record_list)
    # sorted data in different date
    all_rec_dic={}
    sdate0='00000000'
    for fl_rec in record_list:
        sdate=r'%4.4d%2.2d%2.2d' % (fl_rec.yyyy, fl_rec.mm, fl_rec.dd)

        if sdate in all_rec_dic:
            rec_list=all_rec_dic[sdate]
            rec_list.append(fl_rec)
            all_rec_dic.update({sdate:rec_list})
        else:
            rec_list=list()
            rec_list.append(fl_rec)
            all_rec_dic.update({sdate:rec_list})

    # form the planeflight file
    
    head_lines=gen_planeflight_headlines()
    print head_lines
    
    sep_line=gen_planeflight_sep_line()
    
    sep_line=[sep_line]
    
    head_lines=head_lines+sep_line
    # the second the tracers
    sel_tracers=range(1, 42)
    tracer_lines=gen_planeflight_tracer_line(sel_tracers)
    sel_met=['TEMP', 'PSURF']
    met_lines=gen_planeflight_met_line(sel_met)
    record_lines=tracer_lines+met_lines
    ntracer=len(record_lines)
    ntracer_line=r'%2.2d <== The number of geos-chem output TRA=tracer GAMO=met field' % ntracer

    head_lines=head_lines+[ntracer_line]+sep_line+record_lines
    mid_lines=gen_planeflight_midlines()
    head_lines=head_lines+mid_lines
    nheadline=len(head_lines)
    
    end_line=gen_planefight_endline()
    

    
    for sdate in all_rec_dic:
        flnm='planeflight.dat.'+sdate
        out_file=open(flnm, 'w')
        for hline in head_lines:
            out_file.write(hline+'\n')
        
        
        rec_list=all_rec_dic[sdate]
        time_list=list()
        # sorted the time
        for rec in rec_list:
            seconds=rec.hh*3600+rec.mi*60
            time_list.append(seconds)
        short_idx=argsort(time_list)
        line_cnt=0
        
        for idx in short_idx:
            rec=rec_list[idx]
            line_cnt=line_cnt+1
            rec_lin=rec.form_short_line(line_cnt)
            out_file.write(rec_lin+'\n')

        out_file.write(end_line+'\n')
        out_file.close()
        
                      
        
        
    
                
    
    
            
            
          

    
