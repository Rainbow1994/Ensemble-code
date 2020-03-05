""" this module is used to read in the necessary to generate the observations
"""
import field_read.py as frp
import read_orbit as rob
import ak_read as akr

from pylab import *
from numpy import *

def gen_xco2(yyyy, dd, mm):
    # read in gpf
    gpf=frp.setup_field(2003, 1, 10)
    print gpf.gpdict.keys()

    
    lat=[0.0, -30]
    lon=[0.0, 90]
    xpos=[lon, lat, 0]

# the second method,
axis_set=gpf.get_gp_attr('CO2', 'axis_set')
ax_lon=axis_set[0]
ax_lat=axis_set[1]
ax_lz=axis_set[2]
    
lonp1, lonp2, lonwgt=ax_lon.getwgt(lon)
latp1, latp2, latwgt=ax_lon.getwgt(lat)

CO2=gpf.gpdict['CO2']
indx=range(size(latp1))

    
prof1=latwgt[:, newaxis]*CO2[lonp1[:], latp1[:], :]
prof2=(1.0-latwgt[:, newaxis])*CO2[lonp1[:], latp2[:], :]
prof3=latwgt[:, newaxis]*CO2[lonp2[:], latp1[:], :]
prof4=(1.0-latwgt[:, newaxis])*CO2[lonp2[:], latp2[:], :]
co2_prof=lonwgt[:, newaxis]*(prof1+prof2)+\
          (1.0-lonwgt[:, newaxis])*(prof3+prof4)

gp=gpf['PS']

        
    prof1=latwgt[:]*gp[lonp1[:], latp1[:], 0]
    prof2=(1.0-latwgt[:])*gp[lonp1[:], latp2[:], 0]
    prof3=latwgt[:]*gp[lonp2[:], latp1[:], 0]
    prof4=(1.0-latwgt[:])*gp[lonp2[:], latp2[:], 0]
    prof=lonwgt[:]*(prof1+prof2)+\
              (1.0-lonwgt[:])*(prof3+prof4)
    
    sp=lonwgt[:]*(prof1+prof2)+\
              (1.0-lonwgt[:])*(prof3+prof4)
    levels=ax_lz[:]
    levels=array(levels)
    levels=levels+1
    levels=levels.astype(int)
    pres=pm.get_pres(sp, levels)
    semilogy(1.0E6*co2_prof[1,:], pres[1,:])
    ylim([1000.0, 0.6])
    show()

