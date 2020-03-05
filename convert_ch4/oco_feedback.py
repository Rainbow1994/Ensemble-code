from pylab import *
from numpy import *
import time_module as tm
import gp_axis as gax
import netCDF_gen as nf
import numpy.random as rnd
import oco_units as ounit
class geos_varinfo:
    def __init__(self, varname, vartype, vardim, var, varattr=None):
        self.name=varname
        self.type=vartype
        self.dimname=vardim
        self.var=var 
        self.varattr=varattr
        

def ncf_write(ncflnm, dimname, dimtype, dimvar, varnames, vartypes, vars):
    dimTypes=dimtype
    dimVars=dimvar    
    dimNames=dimname
    nf.netCDF_def_dims(ncflnm,dimNames,dimTypes, dimVars)
    tc=list()
    if (type(tc)==type(varnames)):
        nvar=len(varnames)
        for ivar in range(nvar):
            varName=varnames[ivar]
            varType=vartypes[ivar]
            varData=vars[ivar]
                    
            print varName, size(varData), size(dimvar)
            nf.netCDF_var_write(ncflnm,dimNames,varName, varType, varData)

def ncf_write_by_varinfo(ncflnm, dimname, dimtype, dimvar, varinfos, dimattr=None):

    dimTypes=dimtype
    dimVars=dimvar
    # print size(dimVars[0])
    # print size(dimVars[1])
    
    dimNames=dimname
    
    nf.netCDF_def_dims(ncflnm,dimNames,dimTypes, dimVars, dimattr=dimattr)
    tc=list()
    if (type(tc)==type(varinfos)):
        nvar=len(varinfos)
        for varinfo in varinfos:
            varName=varinfo.name
            varType=varinfo.type
            varData=varinfo.var
            vardimnames=varinfo.dimname
            varattr=varinfo.varattr
            # print 'winfo', varName
            # print shape(varData)
            # print vardimnames
            nf.netCDF_var_write(ncflnm,vardimnames,varName, varType, varData,varattr)
            
def ncf_write_cf(ncflnm, diminfos, varinfos, glbattr=None):
    
    """ generate netcdf file according CF-1 conventions
    diminfo: information of dimension
    varino:  information of variables
    
    """
    print 'I am here'
    print ncflnm
    print 'define dims'
    nf.netCDF_def_dims_cf(ncflnm,diminfos, glbattr=glbattr)
    print 'after define dims'
    
    tc=list()
    if (type(tc)==type(varinfos)):
        nvar=len(varinfos)
        for varinfo in varinfos:
            varName=varinfo.name
            varType=varinfo.type
            varData=varinfo.var
            vardimnames=varinfo.dimname
            varattr=varinfo.varattr
            print 'winfo', varName
            print shape(varData)
            print vardimnames
            
            nf.netCDF_var_write(ncflnm,vardimnames,varName, varType, varData,varattr)
            

    

def ncf_read(ncflnm, varnames):
    import netCDF4 as snf 
    ncf=snf.Dataset(ncflnm)
    tc=list()
    if (type(tc)==type(varnames)):
        outvars=list()
        nvar=len(varnames)
        for ivar in range(nvar):
            vname=varnames[ivar]
            var=ncf.variables[vname]
            var=array(var)
            var=squeeze(var)
            outvars.append(array(var))
    else:
        outvars=ncf.variables[varnames]
        outvars=array(outvars)
        outvars=squeeze(outvars)
    ncf.close()
    return outvars
        
    
    
        
    
    
    




    
            
    
