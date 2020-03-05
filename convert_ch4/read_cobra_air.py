from numpy import *
# import standard_atmosphere as stam
# import time_module as tm
class cobra_flight_record:
    def __init__(self, flight_no,line, col_no=23):
        self.flight_no=flight_no
        terms=line.split(',')        
        cur_yyyy, cur_mm, cur_dd=terms[1], terms[2], terms[3]
        self.yyyy, self.mm, self.dd=int(cur_yyyy), int(cur_mm), int(cur_dd)
        
        stime=terms[5]
        self.otime=int(stime)
        
        hh=int(self.otime/3600)
        mi=int(self.otime/60)-60*hh
        ss=self.otime-60*mi-3600*hh
        self.hh=hh
        self.mi=mi
        self.ss=ss
        # lat
        if ('NA' in terms[6]):
            
            self.lat=-999.0
        
            #     if (self.lon<0.0):
            #         self.lon=self.lon+360.0
            
        else:
            self.lat=float(terms[6])
        # lon
        if ('NA' in terms[7]):
            self.lon=-999.0            
        else:
            self.lon=float(terms[7])
        
        # alt
        
        if ('NA' in terms[8]):
            self.alt=-999.0
        else:
            self.alt=float(terms[8])
        
        # vmr
        if ('NA' in terms[col_no]):
            self.vmr=-999.0
        else:
            self.vmr=float(terms[col_no])
        
    def form_short_line(self, line_no):
        sline_no=r'%d' % line_no
        nslin=len(sline_no)
        sline_no=' '*(5-nslin)+sline_no
        
        full_line=sline_no+' '
        
        sname=""
        slen=len(self.flight_no)
        for ip in range(5):
            if (ip < slen):
                sname=sname+self.flight_no[ip]
            else:
                sname=sname+' '
                
        full_line=full_line+sname+' '

        sdate=r'%2.2d-%2.2d-%4.4d' % (self.dd, self.mm, self.yyyy)
        full_line=full_line+sdate+' '

        stime=r'%2.2d:%2.2d' % (self.hh, self.mi)
        full_line=full_line+stime+' '
        
        slat=r'%7.2f' % self.lat
        full_line=full_line+slat+' '

        slon=r'%7.2f' % self.lon
        full_line=full_line+slon+' '

        pres=stam.get_pressure(self.alt/1000.0)
        spres=r'%7.2f' % pres
        full_line=full_line+spres+' '
        svmr=r'%7.2f' % self.vmr
        full_line=full_line+svmr
        
        
        return full_line
        
        
    

def read_cobra_flight_info(flnm, record_list=None):
    fl=open(flnm, "r")
    lines=fl.readlines()
    fl.close()
    flight_rec=list()

    if (record_list==None):
        record_list=list()
    line=lines[0]
    col_names=line.split(',')
    icol=0
    for item in col_names:
        item=item.strip()
        if (item=='CO2'):
            break
        icol=icol+1
    

    for line in lines[1:]:
        line=line.strip()
        new_record=cobra_flight_record('cobra', line,col_no=icol)
        record_list.append(new_record)
            
    return record_list

if (__name__=='__main__'):
    from pylab import *
    flnm='cobra.2003.csv'
    record_list=read_cobra_flight_info(flnm, record_list=None)
    print len(record_list)
    nrec=len(record_list)
    
    z=arange(500, 10000.0, 200.0)
    print z[0:5]
    
    z_bd=z+200.0/2.0
    nz=size(z)
    ncount=zeros(nz)
    prof=zeros(nz,float)
    prof_std=zeros(nz,float)
    
    obs_lat=zeros(nz,float)
    obs_lon=zeros(nz,float)
    
    ts_lat=list()
    ts_lon=list()
    ts_val=list()
    ts_time=list()
    ts_dd=list()
    ts_z=list()
    
    new_day=list()
    for irec in range(nrec):
        cur_rec=record_list[irec]
        if (cur_rec.alt>-990 and cur_rec.lon > -990.0 and cur_rec.lat > -990.0 and cur_rec.vmr > -990.0 and cur_rec.mm==6):
            # print cur_rec.alt, cur_rec.lon, cur_rec.lat
            
            iz=searchsorted(z_bd, cur_rec.alt)
            if (iz >=nz):
                iz=iz-1
            ncount[iz]=ncount[iz]+1
            prof[iz]=prof[iz]+cur_rec.vmr
            prof_std[iz]=prof_std[iz]+cur_rec.vmr**2
            
            obs_lat[iz]=obs_lat[iz]+cur_rec.lat
            obs_lon[iz]=obs_lon[iz]+cur_rec.lon
        
        if (cur_rec.alt>7000.0 and cur_rec.alt<8000.0 and cur_rec.vmr>0.0 and cur_rec.mm==6):
            ts_lat.append(cur_rec.lat)
            ts_lon.append(cur_rec.lon)
            ts_val.append(cur_rec.vmr)
            ts_time.append(cur_rec.otime)
            ts_dd.append(cur_rec.dd)
            ts_z.append(cur_rec.alt)
            
            
    
usd_idx=where(ncount>0)
ncount=ncount[usd_idx]
z=z[usd_idx]
prof=prof[usd_idx]
prof_std=prof_std[usd_idx]

obs_lat=obs_lat[usd_idx]
obs_lon=obs_lon[usd_idx]

prof=prof/ncount

prof_std=sqrt((prof_std-ncount*prof*prof)/ncount)

obs_lat=obs_lat/ncount
obs_lon=obs_lon/ncount


# print prof
subplot(1,2,1)
plot(prof,z, '+')
errorbar(prof,z,xerr=prof_std)
xlim([370, 380])

subplot(1,2,2)
plot(obs_lat,z)
figure(2)
x=array(ts_time)
x=x/(24*3600.0)
ts_dd=array(ts_dd)
x=ts_dd+x

y=array(ts_val)
subplot(2,1,1)
plot(x,y)
# xlim(28.5, 28.7)
subplot(2,1,2)
y=array(ts_lat)

scatter(x,y)

plot(x,y)
# xlim(28.5, 28.7)


show()

    
            
    
        
        
    
                
    
    
            
            
          

    
