""" container (class ) for axis 
    Authors: L. Feng, Edinburgh University
    History: v0.5, 2007.10.28
    History: v0.5, 2007.10.28
this model basically define a grid for representing fields, and
"""

from numpy import *
from scipy import *
from Scientific.Functions.Interpolation import *
import geo_constant as gc
import scipy.weave as weave
gp_fill_val=-999.0
gp_fill_val_int=-999.

             
class gp_axis: 

# the class for one axis 
    def __init__(self, ax_name, ax_grd=None, ax_min=None, ax_max=None):
        self.ax_name=ax_name
        # use dictionary as a container to store additional information
        self.prop={'name':ax_name}
        if (ax_grd==None):
            self.ax_grd=arange(10)
        else:
            self.ax_grd=array(ax_grd)
        if (ax_min==None):
            self.ax_min=min(self.ax_grd)
        else:
            self.ax_min=ax_min
        if (ax_max==None):
            self.ax_max=max(self.ax_grd)
        else:
            self.ax_max=ax_max
            
        val1=self.ax_grd[0]
        self.np=size(self.ax_grd)
        val2=self.ax_grd[-1]
        if (val2<val1):
            self.ax_grd=self.ax_grd[::-1]
        self.prop.update({'np':self.np})
        self.prop.update({'max':self.ax_max})
        self.prop.update({'min':self.ax_min})
    def __getitem__(self, idx):  
        """ override [],  etc called as axis[id]
        """ 
        return self.ax_grd[idx]
    def locate_val(self, val):
        """ get boundary and weight for a given value 
        Auguments: 
        val: values to be checked
        Return:
        pl, pr, wgt: left and right position of the value, and weight
        with respect to the  left boundary:
        Notes:
            if (val>max) the boundary is set to right-most
            if (val<min) the boundary is set to left most
        """
        
        rp=searchsorted(self.ax_grd, val)
        lp=rp-1
        if (val>=self.ax_max):
            rp=self.np-1
            lp=rp
            wgt=1.0
        elif (val<=self.ax_min):
            rp=0
            lp=rp
            wgt=1.0
        else:
            wgt=1.0*(self.ax_grd[rp]-val)/(self.ax_grd[rp]-self.ax_grd[lp])
            
        return lp, rp, wgt
    def locate_vals(self, vals):
        """
            the multiple version of local_val
            Auguments: 
                vals: values to be checked
            Return:
                pl, pr: left and right position of the value(s):
            Notes:
                if (val>max) the boundary is set to right-most
                if (val<min) the boundary is set to left most
                it maybe is quicker than checkpos for one array

             
        """
        p=map(self.locate_val, vals)
        return array(p)
        
    
    def getpos(self, val):

        """ get boundary for given value(s) 
        Auguments: 
        values 
        Return:
        pl, pr: left and right position of the value(s):
        Notes:
        if (val>max) the boundary is set to right-most
        if (val<min) the boundary is set to left most
        it maybe is quicker than checkpos for one array
        
        """

        use_c=False
        sgl_val=False
        aval=array(val)
        tmp_sh=shape(aval)
        
        if (len(tmp_sh)==0):
            # then we choose to return as single value instead of array 
            sgl_val=True

        if (use_c):
            
            x=self.ax_grd

            nxp=size(x)
            
            if (sgl_val):
                nyp=1
                xout=array([aval])
                
            else:
                nyp=size(aval)
                xout=aval
            
            pl=zeros(nyp)
            pr=zeros(nyp)
            
            c_code="""

            int i, j,l;
            j=0;
            
            for (i=0; i<nyp; ++i){
            for (l=0; l<nxp;++l) {
            if (x[l]>=xout[i]) break;
            }
            
            if (l==0){
            pl[i]=0;
            pr[i]=0;
            }

            else if (l>=nxp){
            pl[i]=nxp-1;
            pr[i]=nxp-1;
            }
            
            else {
            pl[i]=l-1;
            pr[i]=l;
            } 
            j=0;
            }
            
            return_val=0;
            
            """

            axgp=weave.inline(c_code,\
                              ['nxp', 'nyp', 'x','xout', 'pl', 'pr'])
            lp=pl.astype(int)
            rp=pr.astype(int)
            # print max(rp), nyp
            
            
            
        else:
            
            rp=searchsorted(self.ax_grd, aval)
            if (sgl_val):
                if (rp==0):
                    lp=0
                elif(rp==self.np):
                    rp=rp-1
                    lp=rp
                else:
                    lp=rp-1
            else:
                lp=where(rp==0, 0, rp-1)
                lp=where(lp==self.np, self.np-1, lp)
                rp=where(rp==self.np, self.np-1, rp)
        
        return lp, rp
    
        
            
    def getwgt(self, val):
        """ get L & R boundary, and their weights for factorgiven value(s) 
         Auguments: 
            val
        Return:
            p1, p2, weight: left, right boundary, and the weight for L boundary
        Notes:
            if (val>max) the boundary is set to right-most
            if (val<min) the boundary is set to left most
        """
        # make sure the [] is appliable
 
        sgl_val=False

        aval=array(val)
        tmp_sh=shape(aval)

        if (len(tmp_sh)==0):
            sgl_val=True
            
            
                        
        p1,p2=self.getpos(aval)

        nval=size(p1)
        wgt=ones(nval, float)
        
        x1=self.ax_grd[p1]
        x2=self.ax_grd[p2]
        
        dx=x2-x1
        
        if (sgl_val):
            if (dx==0):
                wgt=0.0
            else:
                wgt=(x2-aval)/dx
        else:
            wgt=where(dx==0.0, 0.0, 1.0/dx)
            wgt=(x2-aval)*wgt
        
        return p1, p2, wgt
    
    
    def setprop(self, name, value):
        """  assign one property to axis obj
        Auguments:
            name: property name
            value: property value
        """
        self.prop.update({name:value})
    def getprop(self, name):
        """  get one property from axis obj
        Auguments:
            name: property name
        Returns:
            val: property value
        """
        val=self.prop[name]
        return val
    def set_grd(ax_grd):
        """  reset axis grid 
        Auguments:
            name: property name
        Returns:
            val: property value
        """
    
        self.ax_grd=ax_grd
        self.np=size(ax_grd)
        self.max=max(ax_grd)
        self.min=min(ax_grd)
        self.prop.update({'np':self.np})
        self.prop.update({'max':self.max})
        self.prop.update({'min':self.min})


def linear_log_intp(p, gpval, pout, threshold=-2.0):
    """ this function is used to interpolate complicated species such as h2o 
        Arguments:
            p: logp values
            gpval: gp values at given Ps
            pout: the location where the values will interpolated to
            threshold: define the from where the log-linear will be use
        Returns:
            yout, [p1, p2, wgt]: the gpval at pout, and its locations 
        Notes:
            It is assumed that when logp > Threshold, the gpval is a linear function of logp
            when logp < Threshold, the log(gpval) is a linear function of logp

    """    
    ax_p=gp_axis('X', p)
    p1, p2, wgt=ax_p.getwgt(pout)
    yout=wgt*gpval[p1]+(1.0-wgt)*gpval[p2]
    
    ishape=shape(pout)
    
    if (len(ishape)>0):
        idx=where(pout<threshold)
        if (len(idx)>0):
            yout[idx]=wgt[idx]*log(gpval[p1[idx]])+(1.0-wgt[idx])*log(gpval[p2[idx]])
            yout[idx]=exp(yout[idx])
    else:
        if (pout<threshold):
            yout=wgt*logp(gpval[p1])+(1.0-wgt)*log(gpval[p2])
            
    del ax_p
    return yout, [p1, p2, wgt]

def linear_itpl_py(p, gpval, pout, do_exp=False):
    """ this function is used to interpolate complicated species
        Arguments:
            p: logp values
            gpval: gp values at given Ps
            pout: the location where the values will interpolated to
            do_exp: if True, the extrapolation will be done
        Returns:
            yout, [p1, p2, wgt]: the gpval at pout, and its locations 
 
    """    

    
    out_shape=shape(pout)
    # print 'shape p'
    # print shape(p)
    # print shape(pout)
    
    pos=searchsorted(p, pout)
    np=size(p)
    if (do_exp):
        
        if (len(out_shape)>0):
            pos=where(pos==np, np-1, pos)
            pos=where(pos==0, 1, pos)
            pr=pos
            pl=pr-1
            
        else:
            if (pos==np):
                pos=pos-1
                pr=pos
                pl=pos-1
            elif (pos==0):
                pr=1
                pl=0
            else:
                pr=pos
                pl=pr-1
        
        wgt=(p[pr]-pout)/(p[pr]-p[pl])
        
    else:
        if (len(out_shape)>0):
            pr=where(pos==np, pos-1, pos)
            pl=pos-1
            pl=where(pl<0, 0, pl)
            dp=p[pr]-p[pl]
            wgt=where(dp==0.0, 1.0, 1./dp)
            wgt=(p[pr]-pout)*wgt
        else:
            if (pos==np):
                pos=pos-1
                pr=pos
                pl=pos
                wgt=1.0
            elif (pos==0):
                pr=0
                pl=0
                wgt=1.0
            else:
                pr=pos
                pl=pr-1
                dp=p[pr]-p[pl]
                wgt=(p[pr]-pout)/dp
        
        
        out_val=wgt*gpval[pl]+(1.0-wgt)*gpval[pr]
        return out_val, [pl, pr, wgt]

def linear_itpl(p, gpval, pout, do_exp=False):
    """ this function is used to interpolate complicated species
        Arguments:
            p: logp values
            gpval: gp values at given Ps
            pout: the location where the values will interpolated to
            do_exp: if True, the extrapolation will be done
        Returns:
            yout, [p1, p2, wgt]: the gpval at pout, and its locations 
 
    """    
    
    
    out_shape=shape(pout)
    # print 'shape p'
    # print shape(p)
    # print shape(pout)

    wgt=zeros(out_shape,float)
    outval=zeros(out_shape,float)
    nxp=size(p)
    nyp=size(wgt)
    pr=zeros(out_shape, int)
    pl=zeros(out_shape, int)

    gp=gpval
    x=p
    xout=pout
    
    # print nxp, nyp
    
    c_code="""
    int i, j,l;
    j=0;
    for (i=0; i<nyp; ++i){
    for (l=j; l<nxp;++l) {
    
    if (x[l]>=xout[i]) break;
    }
    
    if (l==0){
    wgt[i]=1.0;
    pl[i]=0;
    pr[i]=0;
    outval[i]=gp[l];
    }
    else if (l>=nxp){
    wgt[i]=1.0;
    pl[i]=nxp-1;
    pr[i]=nxp-1;
    outval[i]=gp[nxp-1];
    }
    else {
    pl[i]=l-1;
    pr[i]=l;
    wgt[i]=(x[l]-xout[i])/(x[l]-x[l-1]);
    outval[i]=wgt[i]*gp[l-1]+(1.0-wgt[i])*gp[l];
    } 
    j=l;
    
    }
    
    return_val=0;
    
    """
    axgp=weave.inline(c_code,\
                      ['nxp', 'nyp', 'x', 'xout', 'gp', 'outval', 'pl', 'pr', 'wgt'])
    
            
    return outval, [pl, pr, wgt]

def smp_integration(p, f, p1, p2, use_log=False):
    x=array(p)
    x1=p1
    x2=p2
    
    if (use_log):
        if (x[0]>X[1]):
            x=-log10(x)
            x1=-log10(x1)
            x2=-log10(x2)
        else:
            x=log10(x)
            x1=log10(x1)
            x2=log10(x2)
    idx=where(logical_and(x>x1,  x<x2))
    idx=squeeze(idx)
    bd=array([x1,x2])
    pos=searchsorted(x, bd)
    
    pr=pos[0]
    pl=pr-1
    wgt=(x[pr]-x1)/(x[pr]-x[pl])
    f0=wgt*f[pl]+(1.0-wgt)*f[pr]
    # print shape(f0)
    
    x0=p1
    s=0.0

    for ip in idx:
        f1=f[ip]
        dx=p[ip]-x0
        s=s+0.5*(f0+f1)*dx
        f0=f1
        x0=p[ip]
        
    pr=pos[1]
    pl=pr-1
    wgt=(x[pr]-x1)/(x[pr]-x[pl])
    f1=wgt*f[pl]+(1.0-wgt)*f[pr]
    dx=p2-x0
    s=s+0.5*(f0+f1)*dx
    return s

    
    
              
    
    

if (__name__=='__main__'):
    """ some test on gp_axis """
    a=arange(6.0)
    test_gx=gp_axis('a', a)
    print test_gx[:]
    c=a+rand(6)
    
    p1, p2,wgt=test_gx.getwgt(c)
    print p1, p2,wgt
    c2=wgt*test_gx[p1]+(1-wgt)*test_gx[p2]
    print c
    print c2
    x=arange(0.0, pi, pi/26.0)
    f=sin(x)
    s=smp_integration(x, f, 0.0, 0.5*pi)
    print '='*80
    print 's=sum(sin(x)) ', s
    print 'test_run'
    
    gpval=sin(a)
    vals, pos=linear_itpl(a, gpval, c)
    
    print 'a',  a
    print 'c', c
    print 'vals', vals
    
    vals, pos=linear_itpl_py(a, gpval, c)

    print 'a',  a
    print 'c', c
    print 'vals', vals
    
    
    
    
             

      
