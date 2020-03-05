""" container (class ) for two or three dimenisonal (lon-lat-press etc) data set
    Authors: L. Feng, Edinburgh University
    History: v0.5, 2007.10.28
    History: v0.5, 2007.10.28
this model basically define a grid for representing fields, and
""" 
from numpy import *
from scipy import *
from Scientific.Functions.Interpolation import *
import geo_constant as gc
import gp_axis as gax
             
class gp_field:
    """ general container for geo-physical values in a high-dimension grid 
    
    Variables and routines:
    (1) Storage Species fields: 
    including T, O3, H2O, and, ..,  flexiable:
    (2) Interpolation routines:
    i)  Interpolate the stored field to any point
    ii) Grid data into given grids. 
    Notes:
    the grid transform are limited to 2D grid
    """ 
    def __init__(self, name=None, axis_set=None):
        """ initialization
        Auguments:
        Name: the name of the atomsphere 
        axis_set: a list of the gp_axis
        """ 
        
        if (name==None):
            self.name='Unknown'
        else:
            self.name=name
            
        if (axis_set==None):
            self.naxis=0
            self.axis_set=list()
        else:
            self.naxis=len(axis_set)
            self.axis_set=axis_set
            
        self.gpdict=dict()
        self.prop={}
        self.prop.update({'name':self.name})
        self.prop.update({'ndim':self.naxis})
        self.gp_attr={}
        self.global_attr={}
        

    def add_gp(self, gpname, gp_vals):
        """ add geo-physical values into the data set
        """
        self.gpdict.update({gpname:gp_vals})
    def get_gp(self, gpname):
        """ retrieve the gp field from the data ser
        """
        if (gpname in self.gpdict):
            val=self.gpdict[gpname]
            return val 
        else:
            print "Error: no "+gpname+" is found"
            return None
        
    def set_grid(self, axis_set):
        """ define the grid 
        Auguments: 
            axis_set: list of gp_axis
        
        """ 
        if (self.axis_set<>None):
            del self.axis_set
        
        self.axis_set=axis_set 
        self.naxis=len(axis_set)
        self.prop.update({'ndim':self.naxis})
        
    def gp_interp(self, gpname, rpos, fill_val=None, threshold=0.0):  # pos as single point
        """ Interpolate the gp values to a given location 
            Auguments:
                gpname: the name of the gp 
                rpos: coordinate of the location
                fill_val: if gp[idx] ==fill_val, 
                    the weight of idx will be equal to zero
                threshold: 
                    if the total weight for rpos <threshold, its value 
                    will be set to fill value  
            Returns:
                gp: at the given position
                wgt: weight information as (lp, rp, wgt) for every axis
        """
        
        
        pos_info=list()
        ful_axis_name=gpname+".axis_set"
        
        if (ful_axis_name in self.gp_attr):
            # print 'I am here'
            axis_set=self.gp_attr[ful_axis_name]
        else:
            axis_set=self.axis_set

        naxis=len(axis_set)

        if (len(rpos)<>naxis):
            return gax.gp_fill_value
        
        
        for ix in range(naxis):
            val=rpos[ix]
            ax=axis_set[ix]
            p1, p2,wgt=ax.getwgt(val)
            pos_info.append([p1, p2, wgt])
        
        out_val=0.0
        gp=self.gpdict[gpname]
        # print 'pos_info', pos_info
        nval=2**naxis
        #  print 'nval', nval
        sum_wgt=0.0
        for ii in arange(nval):
            pos=zeros(naxis)
            wgt=1.0
            it=ii
            ip=0
            
            for ix in arange(naxis):
                pt=pos_info[ix]
                isel=mod(it,2)
                it=it/2
                pos[ix]=pt[isel]
                wgt=wgt*abs(isel-pt[2])
            
            ipos=tuple(pos)
            # print ii, ipos
            # print wgt
            
            if (gp[ipos]<>fill_val):
                # print gp[ipos], wgt
                sum_wgt=sum_wgt+wgt
                out_val=out_val+gp[ipos]*wgt
        if (sum_wgt>threshold):
            out_val=out_val/sum_wgt
        else:
            out_val=fill_val
        
        if (naxis==1):
            print out_val, pos_info
        del axis_set
        return out_val, pos_info
    def set_gp_axis_set(self, gp_name, axis_set):
        """ set the gp field to one specified axis_set
            Arguments: 
                gp_name: gp name
                axis_set: the specialized set of axis for the given gp
            Notes:
                the dict of the gp_attr is added one entry as gpname.axis_set
            
        """
        ful_attr_name=gp_name+".axis_set"
        print ful_attr_name
        self.gp_attr.update({ful_attr_name:axis_set})
        print self.gp_attr.keys()
    def remove_gp_axis_set(self, gpname):
        """ remove the specified axis_set from gp property 
            The name of the gp product
        """
        
        ful_attr_name=gp_name+".axis_set"
        if (ful_attr_name in self.gp_attr):
            del self.gp_attr[ful_attr_name]
    def remove_gp_attr(self, gpname, attr_name):
        """ remove one attrib from gp_attr
            Arguments:
                gpname: the name of gp 
                attr_name: the name of the 
        """
        ful_attr_name=gp_name+"."+attr_name
        if (ful_attr_name in self.gp_attr):
            del self.gp_attr[ful_attr_name]
    def remove_gp(self, gpname):
        """ remove one gp values from the storage
            Arguments: 
                gpname: the name of the gp val to be removed
            
        """
        if (gpname in self.gpdict):
                del self.gpdict[gpname]
        # remove the attributes associated with the given gb, which is started as 
        # gpname.
        k_str=gpname+"."
        sl=len(k_str)
        for key in self.gp_attr.keys():
            sl_key=len(key)
            if (sl_key>=sl):
                if (key[0:sl]==k_str[0:sl]):
                    del self.gp_attr[key]
        
        
    def gp_vals(self, gpname, rpos, fill_val=None, threshold=0.0):
        """ Interpolate the gp values to a set of locations 
            Auguments:
                gpname: the name of the gp 
                rpos: coordinates of locations
                fill_val: used to check the elements filled with fill_value
                threshold: if (total weight < = threshold), gp at rpos is filled with fill_value
            Returns:
                gps: at the given position+location information: (lp, rp, wgt) of each val 
                at each axis
                
        """
        
        tf=lambda pos:self.gp_interp(gpname, pos, fill_val=gax.gp_fill_val, threshold=threshold)
        rvals=map(tf, rpos)
        del tf
        return rvals
      
        

    def gp_interp_2d(self, gpname, rpos_set): 
        """ Interpolate the gp values to a given locations in a two dimensional grid 
            Auguments:
                gpname: the name of the gp 
                rpos_set: coordinate of the set of locations 
                    (i.e., [[P0], [P1],...]
            Returns:
                gp_val at the locations
                pos_info: list of weighting information as [lpx, rpx, wgx,lpy, rpy, wgy]
        """
        # callable for []
        rset=array(rpos_set)
        pt=rset[0]
        if (size(pt)==1):
            rset=array([rset])
        pos_info=list()
        dims=shape(rset)
        npt=dims[0]
        
        gpv=zeros(npt, float)
        gp=self.gpdict[gpname]
        if (npt==1):
            rpos=rset[0]
            print 'rpos', rpos, shape(rpos)
            
            xp1, xp2, wgx=self.axis_set[0].getwgt(rpos[0])
            yp1, yp2, wgy=self.axis_set[1].getwgt(rpos[1])
            gpv=wgx*(wgy*gp[xp1,yp1]+(1.0-wgy)*gp[xp1, yp2])+ \
                     (1.0-wgx)*(wgy*gp[xp2,yp1]+(1.0-wgy)*gp[xp2, yp2]) 
            pos_info.append([xp1, xp2, wgx, yp1, yp2, wgy])
            return gpv, pos_info
        
        rset=rpos_set
        
        for ip in range(npt):
            rpos=rset[ip]
            xp1, xp2, wgx=self.axis_set[0].getwgt(rpos[0])
            yp1, yp2, wgy=self.axis_set[1].getwgt(rpos[1])
            gpv[ip]=wgx*(wgy*gp[xp1,yp1]+(1.0-wgy)*gp[xp1, yp2])+ \
                     (1.0-wgx)*(wgy*gp[xp2,yp1]+(1.0-wgy)*gp[xp2, yp2])
            pos_info.append([xp1, xp2, wgx, yp1, yp2, wgy])           
            
        return gpv, pos_info
  
        
    
    def gp_axis_transform_2d(self, gpname, rep_ax_names, new_axis_set):

        """ retrieve gp field after transform  from one set of axis to another  
            Auguments:
                gpname: the name of the gp 
                rep_ax_names: the names of the axis will be transformed
                new_ax_set:   the set of new axis  
            Returns:
                gp vals at the grid point of new axis
        """
        gp=array(self.gpdict[gpname])
        naxis=size(rep_ax_names)
        
        for iax in range(naxis):
            name=rep_ax_names[iax]
            
            ix=0
            for ax in self.axis_set[:]:
                if (ax.ax_name==name):
                    break
                ix=ix+1

            new_axis=new_axis_set[iax]
            p1, p2, wgt=ax.getwgt(new_axis[:])
            nx=size(p1[:])
            idx=arange(nx)
            new_gp=zeros([nx, len(gp[0,:])], float)
                        
            # print 'p1', p1
            # print 'p2', p2
            m_wgt=zeros([nx, nx], float)
            m_wgt_1=zeros([nx, nx], float)
            m_wgt_r=array(m_wgt)
            m_wgt[idx[:], idx[:]]=wgt[idx[:]]
            m_wgt_r[idx[:], idx[:]]=1.0-wgt[idx[:]]
            # print shape(m_wgt)
            
            if (ix==0):  
                gp1=gp[p1[:],:]
                gp2=gp[p2[:],:]
                # print shape(gp1)
                
                new_gp=dot(m_wgt,gp1)+dot(m_wgt_r,gp2)
            elif (ix==1):
                gp1=gp[:, p1[:]]
                gp2=gp[:, p2[:]]
                new_gp=dot(gp1, m_wgt)+dot(gp2,m_wgt_r)
            
            del m_wgt
            del m_wgt_1
            del gp1
            del gp2
            
            gp=new_gp
        
         
        return new_gp

    def get_axis_transform_2d(self, gpname, rep_ax_names, new_axis_set):

        """ retrieve gp field after transform  from one set of axis to another  
            Auguments:
                gpname: the name of the gp 
                rep_ax_names: the names of the axis will be transformed
                new_ax_set:   the set of new axis  
            Returns:
                gp vals at the grid point of new axis
        """
        gp=array(self.gpdict[gpname])
        naxis=size(rep_ax_names)
        transf_m=list()
        
        
        for iax in range(naxis):
            name=rep_ax_names[iax]
            
            ix=0
            for ax in self.axis_set[:]:
                if (ax.ax_name==name):
                    new_axis=new_axis_set[iax]
                    break
                ix=ix+1
            
            p1, p2, wgt=ax.getwgt(new_axis[:])
            nx=size(p1[:])
            mtr=[ix, nx, p1, p2, wgt]
            transf_m.append(mtr)
            
            
            
            
        if (naxis<2):
            ix=1-ix
            ax=self.axis_set[ix]
            nx=size(ax[:])
            p1=arange(nx)
            p2=p1
            wgt=zeros(nx, float)
            wgt=wgt+1.0
            
            # print shape(m_wgt)
            mtr=[ix, nx, p1, p2, wgt]
            transf_m.append(mtr)
            
         
        return transf_m

    
    def gp_check_negative(self, gpname, do_change=True, fill_value=None, scale_factor=1.0):
        """ change the negative value to some fixed value (fill_value), 
            and scale to some value 
        """
        gp=array(self.gpdict[gpname])
        idx=where(gp<0.0)
        if (fill_value<>None):
            gp[idx]=fill_value
        else:
            gp[idx]=abs(gp[idx])*scale_factor
            
        if (do_change):
            self.gpdict.update(gpname,gp)
         # a fake value to use
         
        return gp


    def gp_check_negative_2d(self, gpname, do_change=True, scale_factor=1.0, yaxis=1):
        """ change the negative value to some fixed value (fill_value), 
            and scale to some value at the nearby vertical value
            
        """
        gp=array(self.gpdict[gpname])
        nx, ny=shape(gp)

        if (yaxis==1):
            for ix in range(nx):
                idx=where(gp[ix, :]>0.0)
                if (len(idx)==0): 
                    gp[ix,:]=1.0E-15 # one very small value
                else:
                    pos=idx[0]
                    npos=pos
                    for iy in range(pos+1,ny):
                        if (gp[ix, iy]<0.0):
                            gp[ix, iy]=scale_factor*gp[ix,iy-1]
                    for iy in arange(pos, 0, -1):
                        if (gp[ix, iy]<0.0):
                            gp[ix, iy]=scale_factor*gp[ix,iy+1]
        else:
                
            for ix in range(nx):
                idx=where(gp[:, ix]>0.0)
                if (len(idx)==0): 
                    gp[:,ix]=1.0E-15 # one very small value
                else:
                    pos=idx[0]
                    npos=pos
                    for iy in range(pos+1,ny):
                        if (gp[iy, ix]<0.0):
                            gp[iy, ix]=scale_factor*gp[iy-1, ix]
                    for iy in arange(pos-1, -1, -1):
                        if (gp[iy, ix]<0.0):
                            gp[iy, ix]=scale_factor*gp[iy+1,iy]
        if (do_change):
            self.gpdict.update({gpname:gp})
        return gp


    def check_negative_vals_2d(self, gpval, scale_factor=1.0, yaxis=1):
        """ change the negative value to some fixed value (fill_value), 
            and scale to some value at the nearby vertical value
            
        """
        gp=array(gpval)
        nx, ny=shape(gp)
        
        if (yaxis==1):
            for ix in range(nx):
                idx=where(gp[ix, :]>0.0)
                if (len(idx)==0): 
                    gp[ix,:]=1.0E-15 # one very small value
                else:
                    pos=idx[0]
                    npos=pos
                    for iy in range(pos+1,ny):
                        if (gp[ix, iy]<0.0):
                            gp[ix, iy]=scale_factor*gp[ix,iy-1]
                    for iy in arange(pos, 0, -1):
                        if (gp[ix, iy]<0.0):
                            gp[ix, iy]=scale_factor*gp[ix,iy+1]
        else:
                
            for ix in range(nx):
                idx=where(gp[:, ix]>0.0)
                if (len(idx)==0): 
                    gp[:,ix]=1.0E-15 # one very small value
                else:
                    pos=idx[0]
                    npos=pos
                    for iy in range(pos+1,ny):
                        if (gp[iy, ix]<0.0):
                            gp[iy, ix]=scale_factor*gp[iy-1, ix]
                    for iy in arange(pos-1, -1, -1):
                        if (gp[iy, ix]<0.0):
                            gp[iy, ix]=scale_factor*gp[iy+1,iy]
        return gp
        
    
    def gp_get_prof(self, gpname, xpos, xaxis=0, fill_val=None, threshold=0.0):
        """ interpolate the gp values to at the given [xvalx, yvals]
        Arguments:
        gpname: the gpname will be interpolate
        [fixed_xl, :, fixed_xr]: form the index set for matrix of gpname, but
        xaxis: decided which axis is ignored in the representations 
        fill_val: used to check invalid elements
        threshold: if the tolal weight is smaller than threshold, gp_value is invalid
        Notes:
        In principle, the gp val could be in any shape
        """
        pos_info=list()
        
        ip=0
        # to handle field at grid different from the default # 
        ful_axis_name=gpname+".axis_set"
        if (ful_axis_name in self.gp_attr):
            axis_set=self.gp_attr[ful_axis_name]
        else:
            axis_set=self.axis_set
        
        ax=axis_set[xaxis]
        naxis=size(axis_set)
        ref_x=ax[:]
        gp_prof=zeros(size(ref_x), float)
        sum_wgt=array(gp_prof)
        # print 'size', size(gp_prof)
        pos_info=list()
        
        for ix in range(0, naxis):
            # find the grid number
            if (ix<>xaxis):
                val=xpos[ip]
                ax=self.axis_set[ix]
                p1, p2,wgt=ax.locate_val(val)
                pos_info.append([p1, p2, wgt])
                ip=ip+1
        gp=self.gpdict[gpname]
        # print 'pos_info', pos_info
        nval=2**(naxis-1)
        
        #  print 'nval', nval
        nx=size(ref_x)
        idx=arange(nx)
        
        for ii in arange(nval):
            pos_xl=()
            pos_xr=()
            wgt=1.0
            it=ii
            ip=0
            
            for ix in arange(naxis):
                if (ix<>xaxis):
                    pt=pos_info[ip]
                    isel=mod(it,2)
                    it=it/2
                    if (ix<xaxis):
                        pos_xl=pos_xl+tuple([pt[isel]])
                    if (ix>xaxis):
                        pos_xr=pos_xr+tuple([pt[isel]])
                    wgt=wgt*abs(isel-pt[2])
                    ip=ip+1
            
            tuple_pos=self.myslice_sgl(pos_xl, None, pos_xr)
            # print tuple_pos
            # print shape(gp)
            
            gp_tmp=gp[tuple_pos]
            if (size(gp_tmp)>1):
                gp_tmp=squeeze(gp_tmp)
                usd_idx=where(gp_tmp<>fill_val)
                # print gp_tmp
                # print shape(gp_prof[usd_idx])
                # print shape(gp_tmp[usd_idx])
                
                sum_wgt[usd_idx]=sum_wgt[usd_idx]+wgt
                gp_prof[usd_idx]=gp_prof[usd_idx]+wgt*gp_tmp[usd_idx]
                    
            else:
                if (gp_tmp<>fill_val):
                    sum_wgt=sum_wgt+wgt
                    gp_prof=gp_prof+wgt*gp[tuple_pos]
                    
            
        if (fill_val>None):
            gp_prof=where(sum_wgt>threshold, gp_prof/sum_wgt, fill_val)
        else:
            gp_prof=where(sum_wgt>threshold, gp_prof/sum_wgt, gax.gp_fill_val)
        
        del axis_set
        return ref_x, gp_prof 

    
    def __getitem__(self, gpname):
        return self.gpdict[gpname]

    def get_axis_set(self):
        return self.axis_set
    def get_axis_names(self):
        names=list()
        for ax in self.axis_set:
            names.append(ax.ax_name)
        return names
    
    def set_gp_attr(self, gpname, name, value):
        """  assign one attrib to one gp product 
        Auguments:
            name: property name
            value: property value
        Notes:
            the gp attribute is named as gpname.attr
        """
        ful_name=gpname+"."+name
        self.gp_attr.update({ful_name:value})
    def set_gp_attrs(self, gpname, attrs):
        """  assign one attrib to one gp product 
        Auguments:
            name: property name
            value: property value
        Notes:
            the gp attribute is named as gpname.attr
        """
        for name in attrs.keys():
            val=attrs[name]
            ful_name=gpname+"."+name
            self.gp_attr.update({ful_name:val})
        
        
    def get_gp_attr(self, gpname, name):
        """  get one property from axis obj
        Auguments:
            name: property name
        Returns:
            val: property value
        """
        ful_name=gpname+"."+name
        val=self.gp_attr[ful_name]
        return val

    def set_to_fill_val(self, idx, gp_name, fill_value):
        gp=self.ax_dict[gpname]
        gp[idx]=fill_value
        self.ax_dict.update(gpname, gp)
    

    def interp_along_axis(self, gpname, xval, axis=0):
        """ interpolate gp field to a given x  (choose axis)
            Arguments: 
                gpname: name of the gp values
                xval:  the location of the x values
                axis: the choose between x and y 
            Returns:
                prof_gp: the array of gp value at x 
                [xp1, xp2, wgt]: the location and weight factor 
            Notes:
                It is a 2D (fast) version. 
        """ 

        
        
        ful_axis_name=gpname+".axis_set"
        if (ful_axis_name in self.gp_attr):
            axis_set=self.gp_attr[ful_axis_name]
        else:
            axis_set=self.axis_set
        
        ax=axis_set[axis]
        xp1, xp2,wgt=ax.getwgt(xval)
        sl=tuple([slice(None, None, None)])
        pos_l=tuple()
        pos_r=tuple()
        for ix in range(len(axis_set)):
            if (ix==axis):
                pos_l=pos_l+tuple([xp1])
                pos_r=pos_r+tuple([xp2])
            else:
                pos_l=pos_l+sl
                pos_r=pos_r+sl
        
        
        gp=self.gpdict[gpname]
        
        prof_gp=wgt*gp[pos_l]+(1.0-wgt)*gp[pos_r]
        
        return prof_gp, [xp1, xp2, wgt]
    
    def myslice(self, pos_xl, idx, pos_xr):
        """ return a set of index to access elements of n-d array
            Arguments:
                pos_xl, pos_xr: the tuple of index at the left and right side of id
            Returns:
                ps: a list of tuple of the n-d index  
        """
        f=lambda ix:self.myslice_sgl(pos_xl, ix, pos_xr) 
        ps=map(f,idx)
        # ps=array(ps)
        del f
        return  ps
    
    def myslice_sgl(self, pos_xl, id, pos_xr):
        """ Form a myslice to access element of n-dimension array
            Arguments:
                pos_xl, pos_xr: the tuple of index at the left and right side of id
            Returns:
                sl: the tuple of the n-d index  
                
        """
        if (id==None):
            slp=tuple([slice(None, None, None)])
        else:
            slp=tuple([id])
        sl=pos_xl+slp
        sl=sl+pos_xr
        return sl
        
        # print sl
    def save_to_netcdf(self, gpfile, gpname):
        """ dump the data to the netcdf file 
        """
        import netCDF_gen as nf
        
        dimTypes=list()
        dimVars=list()    
        dimNames=list()
        for ax in self.axis_set:
            dimTypes.append('f')
            axvar=array(ax[:])
            axname=ax.getprop('name')
            dimNames.append(axname)
            dimVars.append(axvar)
        
        nf.netCDF_def_dims(gpfile,dimNames,dimTypes, dimVars)
            
        varName=gpname
        varType='f'
        
        varData=self.gpdict[gpname]
        
        nf.netCDF_var_write(gpfile,dimNames,varName, varType, varData)
            
    def set_global_attr(self, attr_name, val):
        """ set some global attribute into the 
            Arguments:
                attr_name: the attribute name
                val: the value of the attribute
            
        """
        self.global_attr.update({attr_name:val})
    def remove_global_attr(self, attr_name):
        """ remove global attr 
            Arguments:
                attr_name: the name of the attribute to be removed 
        """
        if (attr_name in self.global_attr):
            del self.global_attr[attr_name]
    def get_global_attr(self, attr_name):
        """ read global attribute 
            Arguments:
                attr_name: the name of the attribute to be read
            return:
                the attribute value
        """
        if (attr_name in self.global_attr):
            val=self.global_attr[attr_name]
            return val
        else:
            return None
    

if (__name__=="__main__"):
    """ test of the gp field of 6D 
        
    """
    print " test 6D temperature field "
    p=arange(-3, 3.1, 1./6) # pres
    lon=array([0]) # longitude
    lat=arange(-90, 90.1,30) # latitudee 
    lst=arange(0, 24, 6)   # local solar time
    lsz=array([0])           # local solar zenith angle
    lt=array([0,1])          # time in year
    ax_p=gax.gp_axis('P', ax_grd=p)
    ax_lon=gax.gp_axis('lon', ax_grd=lon)
    ax_lat=gax.gp_axis('lat', ax_grd=lat)
    ax_lst=gax.gp_axis('lst', ax_grd=lst)
    ax_lsz=gax.gp_axis('lsz', ax_grd=lsz)
    ax_lt=gax.gp_axis('lt', ax_grd=lt)
    tf=gp_field('T', axis_set=[ax_p, ax_lon, ax_lat, ax_lst, ax_lsz, ax_lt])
    print '------------- set up the axis set ----------------- '
    print 'ax_p: ', ax_p[:]
    print 'ax_lon:', ax_lon[:]
    print 'ax_lat: ', ax_lat[:]
    print 'ax_lst: ', ax_lst[:]
    print 'ax_lsz: ', ax_lsz[:]
    print 'ax_lt: ', ax_lt[:]
    print '----- set up a Temperature field with meridional gradient of 1.5 K per 30 Deg from tropical ------'
    T=zeros([size(p),size(lon), size(lat), size(lst), size(lsz), size(lt)], float)
    T=T+300.0
    # tilt in z 
    for ix in arange(1, 7):
        T[ix,:,:,:,:,:]=T[ix-1,:,:,:,:,:]-20.0
    for ix in arange(7, 19):
        T[ix,:,:,:,:,:]=T[ix-1,:,:,:,:,:]+10.0
    for ix in arange(19, size(p)):
        T[ix,:,:,:,:,:]=T[ix-1,:,:,:,:,:]-5.0
    # tilt in lat
    for ix in arange(size(lat)):
        T[:,:,ix,:,:,:]=T[:,:,ix,:,:,:]-lat[ix]/20.0
    
    
    tf.add_gp('T', T)
    print 'shape T', shape(T)
    print '------------ test gp interpolation to points: -------- '
    pval=-2.2
    yval=0.0
    p1=[pval, 0, yval, 1.0, 1.0, 1.0]
    pl, pr, pwgt=ax_p.getwgt(pval)
    yl,yr, ywgt=ax_lat.getwgt(yval)
    print 'p1:', p1, 'pos in p-grid', pl, pr, pwgt, 'pos in lat-grid', yl, yr, ywgt
    pval=-2.2
    yval=30.0
    p2=[pval, 0, yval, 1.0, 1.0, 1.0]
    pl, pr, pwgt=ax_p.getwgt(pval)
    yl,yr, ywgt=ax_lat.getwgt(yval)
    print 'p2:', p2, 'pos in p-grid', pl, pr, pwgt, 'pos in lat-grid', yl, yr, ywgt
    print 'use gp_vals to get the interpolated vals'
    tx=tf.gp_vals('T', [p1,p2])   
    tx0=tx[0]
    tx1=tx[1]
    
    print 'gp_val at p0:', tx0[0]
    print 'gp_val at p1:', tx1[0]
     
    print '------------ extract gp values at different pressures -------- '
    p3=p1[1:]

    print 'At [lon, lat, lst, lsz, lt]:', p3
    xp, tp=tf.gp_get_prof('T',p3)
     
    print 'pressure:', xp
    print 'gp values:', tp
    p3=p2[1:]
    print 'At [lon, lat, lst, lsz, lt]:', p3
    xp, tp=tf.gp_get_prof('T',p3)
     
    print 'pressure:', xp
    print 'gp values:',tp
    
 
    print '------------ extract gp values at different latitude -------- '
    p3=p1[1:]
    xaxis=2
    p3[0:xaxis]=p1[0:xaxis]
    p3[xaxis:]=p1[xaxis+1:]
    
    print 'At [p, lat, lst, lsz, lt]:', p3
    xp, tp=tf.gp_get_prof('T',p3,xaxis=xaxis)
    
    print 'lat:', xp
    print 'gp values:', tp
    
    print '-----set T at pressure level of 4 to be invalid-----'
    T[4,0, 3:5, ...]=-999.0
    tf.add_gp('T', T)
    
    p3=p1[1:]
    
    print 'At [lon, lat, lst, lsz, lt]:', p3
    xp, tp=tf.gp_get_prof('T',p3)
    print 'pres:', xp
    print 'gp values:', tp
    
    print ' when no fill value is check' 
    tx=tf.gp_vals('T', [p1])
    print tx[0][0]
    
    print ' when fill  value is set' 
    tx=tf.gp_vals('T', [p1], fill_val=-999.0, threshold=0.2)
    print tx[0][0]
    
    print '--------extract gp values at different latitude with the value is set  '
    p3=p1[1:]
    xaxis=2
    p3[0:xaxis]=p1[0:xaxis]
    p3[xaxis:]=p1[xaxis+1:]
    
    print 'At [p, lat, lst, lsz, lt]:', p3
    xp, tp=tf.gp_get_prof('T',p3,xaxis=xaxis, fill_val=-999.0, threshold=0.9)
    print 'lat:', xp
    print 'gp values:', tp
    
    print 'Get the field at given pressure'
    psel=0.888
    txp, ttp=tf.interp_along_axis('T', psel)
    print 'the shape of the new data set:', shape(txp)
    
    print '------- setup one 1D array gp values -----'
    ax2=gax.gp_axis('X2', xp)
    p_1d=[-45.0]
    tf.add_gp('T2', tp)
    tf.set_gp_axis_set('T2', [ax2])
    tu=tf.gp_vals('T2', [p_1d])
    print tu
    print'------ del T2 from the array ------'
    print 'before'
    print tf.gpdict.keys()
    print tf.gp_attr.keys()
    tf.remove_gp('T2')
    print 'after' 
    print tf.gpdict.keys()
    print tf.gp_attr.keys()
    
