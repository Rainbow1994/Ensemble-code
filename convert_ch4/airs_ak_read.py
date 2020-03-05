""" this module is used to read in climatology data set 
    Authors: Dr. Liang Feng, University of Edinburgh
    History: v0.20, Nov.16, 2007
    Notes: 
      It is used to read the 'fake' average kernal 
""" 

from numpy import *
import gp_field as gpf
import time_module as tm
import gp_axis as gax
import geos_chem_def as gcd
def_ak_path=gcd.oco_ak_path
def_ak_prefix="ak"
def_axis_keys=['lat', 'Logp']  
def_axis_keys.reverse()
def_ak_lats=[15, 45, 75]
def_ak_lat_names=['trop', 'mid',  'polar']
def_ak_name='AIRS'




# def_ak_pres.reverse()
# print def_ak_pres

class average_kernal(gpf.gp_field):
    """ storage for average kernal data
    """
    
    def __init__(self, \
                 gpname=None, do_debug=False):
        gpf.gp_field.__init__(self, def_ak_name, None)
        self.read_airs_ak(do_debug=do_debug)
        
    def read_airs_ak(self, fpath='./airs', do_debug=False):
        """ read into the average kernal data
        Arguments:
        surface the surface type
        """
        
        ak_lats=array(def_ak_lats)
        for ilat in range(size(ak_lats)):
            fname=def_ak_prefix+"_"+def_ak_lat_names[ilat]+".dat"
            fc=open(fpath+"/"+fname, "r")
            
            
            if (ilat==0):
                line1=fc.readline()
                lines=fc.readlines()
                fc.close()
                ak_pres=list()
                data=list()

            ak_val=list()
            for line in  lines:
                terms=line.split()
                if (ilat==0):
                    ak_pres.append(float(terms[0]))
                ak_val.append(float(terms[1]))
                
            data.append(array(ak_val))

        ak_pres=array(ak_pres)
        npres=size(ak_pres)
        nlat=size(ak_lats)

        data=array(data)
        data=reshape(data, [nlat,npres])
        
        
        ax_lat=gax.gp_axis('sza', ak_lats)
        ax_logp=gax.gp_axis('Logp', log10(ak_pres))
        
        axis_set=[ax_lat, ax_logp]
        gpname=def_ak_name
        gpunit='NONE'
        self.add_gp(gpname, data)
        self.set_grid(axis_set)
        self.set_gp_attr(gpname, 'UNIT', gpunit)
        del data

    def get_ak_prof(self, rpos):
        """ this function is used to get a profile vs pressure or vertical grid
        Arguments:
        the name of the gp to be read
        """
        gpname=def_ak_name
        ref_x, profs=self.gp_get_prof(gpname, rpos, xaxis=1) # choose pressure
        
        return ref_x, profs


if __name__=='__main__':
    """ that is a test
    """
    from pylab import *
    from numpy import *
    ak=average_kernal('ocean')
    rpos=list()
    rpos=[10.0]
    logp, prof=ak.get_ak_prof(rpos)
    # print shape(logp)
    #  print shape(prof)
    
    data=ak.get_gp(def_ak_name)
    pres=10**(logp)

    # subplot(1,2,1)
    # semilogy(prof, pres)
    # semilogy(p1, pres, '--')
    # semilogy(p2, pres, '--')
    # ylim([1000.0, 1.0])
    
    semilogy(prof, pres)
    
    ylim([1000.0, 10.0])
    title('airs kernel')
    savefig('oco_ak.png')
    show()
    
    
    
    
    
    
    
    

   
    
    
    
    
