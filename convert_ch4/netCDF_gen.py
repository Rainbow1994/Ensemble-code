from numpy import *
# from Scientific.IO.NetCDF import *
import netCDF4 as snf 
def var_to_netCDF(filename,dimNames,dims, var_name, var):
    file_nc=snf.Dataset(filename, 'w')
    ndim=size(dimNames)
    nsizes=list()
    vcontain=list()
    for id in arange(ndim):
        dvar=dims[id]
        dname=dimNames[id]
        dsize=size(dvar)
        dim_1d=(dname,)
        file_nc.createDimension(dname,dsize)
        var1d=file_nc.createVariable(dname, 'f', dim_1d)
        # print shape(var1d)
        # print var1d[:]
        # print shape(dvar)
        # print dvar
        nsizes.append(dsize)
        for i in range(dsize):
            var1d[i]=float(dvar[i])
            print var1d[i]
        
        # print var1d[:]
        setattr(var1d, '_fill_value', -999.0)

        if (dname=='level'):
            setattr(var1d, 'units', 'hPa')
        elif (dname=='longitude'):
            setattr(var1d, 'units',  "degrees_east")
        elif (dname=='lat'):
                setattr(var1d, 'units',  "degrees_north")
        vcontain.append(var1d)
    
    dim_nd=tuple(dimNames)
    # print dim_nd
    cdf_var=file_nc.createVariable(var_name, 'f', dim_nd)

    # print shape(cdf_var)
    # print cdf_var[0,0]
    # print varname
    # print shape(cdf_var)
    
    if (ndim==1):
        n1=nsizes[0]
        for i in range(n1):
            cdf_var[i]=float(var[i])
    elif (ndim==2):
        n1,n2=nsizes[0], nsizes[1]
        # print n1, n2
        
        for i in range(n1):
            for j in range(n2):
           #     print i,j
                cdf_var[i,j]=float(var[i,j])
    
    elif (ndim==3):
        n1,n2, n3=nsizes[0], nsizes[1], nsizes[2]
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    cdf_var[i,j,k]=float(var[i,j,k])
        
    elif (ndim==4):
        n1,n2, n3, n4=nsizes[0], nsizes[1], nsizes[2], nsizes[3]
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    for l in range(n4):
                        cdf_var[i,j,k, l]=float(var[i,j,k, l])
                    
    elif (ndim==5):
        n1,n2, n3, n4, n5=nsizes[0], nsizes[1], nsizes[2], nsizes[3], nsizes[4]
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    for l in range(n4):
                        for m in range(n4):
                            cdf_var[i,j,k, l,m]=float(var[i,j,k, l,m])

    
    
    elif (ndim==6):
        n1,n2, n3, n4, n5, n6=nsizes[0], nsizes[1], nsizes[2], nsizes[3], nsizes[4], nsizes[5]
        for i in range(n1):
            for j in range(n2):
                for k in range(n3):
                    for l in range(n4):
                        for m in range(n4):
                            for n in range(n5):
                                cdf_var[i,j,k, l,m,n]=float(var[i,j,k, l,m,n])

   
    setattr(cdf_var, '_fill_value', -999.0)
    
    file_nc.close()

def netCDF_def_dims(filename,dimNames,dimTypes, dimVars, conventions=None, dimattr=None):
    file_nc=snf.Dataset(filename, 'w')
    ndim=size(dimNames)
    nsizes=list()
    vcontain=list()
    
    if (conventions==None):
        setattr(file_nc, "Conventions", "CF-1.0")
    
    # print ndim
    # print dimNames
    # print dimVars
    
    for id in range(ndim):
        dvar=dimVars[id]
        
        dname=dimNames[id]
        dsize=size(dvar)
        dim_1d=(dname,)
        # print dname
        file_nc.createDimension(dname,dsize)
        st=dimTypes[id]
        var1d=file_nc.createVariable(dname, st, dim_1d)
        # print shape(var1d)
        # print var1d[:]
        # print shape(dvar)
        # print dvar
        nsizes.append(dsize)
        for i in range(dsize):
            var1d[i]=float(dvar[i])
            # print var1d[i]
            
        # print var1d[:]
        setattr(var1d, '_fill_value', -999.0)

        
        if (dname=='level'):
            # setattr(var1d, 'units', '1')
            setattr(var1d, 'standard_name', 'atmosphere_hybrid_sigma_pressure_coordinate')
            
        elif (dname=='longitude'):
            setattr(var1d, 'units',  "degrees_east")
            setattr(var1d, 'long_name', 'Longitude, positive east')
            setattr(var1d,  'standard_name', 'longitude')
            
        elif (dname=='latitude'):
            setattr(var1d, 'units',  "degrees_north")
            setattr(var1d, 'long_name', 'Latitude, positive north')
            setattr(var1d,  'standard_name', 'latitude')
        elif (dname=='time'):
            setattr(var1d, 'long_name', 'time')
            setattr(var1d, 'standard_name', 'time')
            
        if (dimattr<>None):
            varattr=dimattr[id]
            if (varattr<>None):
                for attrname in varattr:
                    attrval=varattr[attrname]
                    setattr(var1d, attrname, attrval)
        
        vcontain.append(var1d)
        
        file_nc.sync()
    file_nc.close()
    
    
def netCDF_def_dims_cf(filename,diminfos, glbattr=None):
    
    file_nc=snf.Dataset(filename, 'w')
    ndim=len(diminfos)
    
    nsizes=list()
    vcontain=list()
    if (glbattr<>None):
        if (not "Conventions" in glbattr):
            setattr(file_nc, "Conventions", "CF-1.0")
        
        for attrname in glbattr:
            attrval=glbattr[attrname]
            setattr(file_nc, attrname, attraval)
    else:
        setattr(file_nc, "Conventions", "CF-1.0")
        
    
    for dm in diminfos:
        # print dm.name
        
        dvar=dm.var
        dname=dm.name
        dsize=size(dvar)
        dattr=dm.varattr
        
        dim_1d=(dname,)
        # print dname
        file_nc.createDimension(dname,dsize)
        st=dm.type
        var1d=file_nc.createVariable(dname, st, dim_1d)
        
        nsizes.append(dsize)

        
        for i in range(dsize):
            var1d[i]=float(dvar[i])
            # print var1d[i]
            
        # print var1d[:]
        setattr(var1d, '_fill_value', -999.0)

        
        if (dname=='level'):
            if (dattr<>None):
                if (not 'units' in dattr):
                    setattr(var1d, 'units', 'L')
                    
                if (not 'standard_name' in dattr):
                    setattr(var1d, 'standard_name', 'atmosphere_hybrid_sigma_pressure_coordinate')
            else:
                setattr(var1d, 'units', 'L')
                setattr(var1d, 'standard_name', 'atmosphere_hybrid_sigma_pressure_coordinate')
                
        elif (dname=='longitude' or dname=='lon'):
            if (dattr<>None):
                if (not 'units' in dattr):
                    setattr(var1d, 'units',  "degrees_east")
                if (not 'long_name' in dattr):   
                    setattr(var1d, 'long_name', 'Longitude, positive east')
                if (not 'standard_name' in dattr):       
                    setattr(var1d,  'standard_name', 'longitude')
            else:
                setattr(var1d, 'units',  "degrees_east")
                setattr(var1d, 'long_name', 'Longitude, positive east')
                setattr(var1d,  'standard_name', 'longitude')
        elif (dname=='latitude' or dname=='lat'):
            if (dattr<>None):
                if (not 'units' in dattr):
                    setattr(var1d, 'units',  "degrees_north")
                if (not 'long_name' in dattr):   
                    setattr(var1d, 'long_name', 'Latitude, positive north')
                if (not 'standard_name' in dattr):       
                    setattr(var1d,  'standard_name', 'latitude')
            else:
                setattr(var1d, 'units',  "degrees_north")
                setattr(var1d, 'long_name', 'Latitude, positive north')
                setattr(var1d,  'standard_name', 'latitude')
        elif (dname=='time'):
            if (dattr<>None):
                if (not 'long_name' in dattr): 
                    setattr(var1d, 'long_name', 'time')
                if (not 'standard_name' in dattr):  
                    setattr(var1d, 'standard_name', 'time')
            else:
                setattr(var1d, 'long_name', 'time')
                setattr(var1d, 'standard_name', 'time')
        if (dattr<>None):
            for attrname in dattr:
                attrval=dattr[attrname]
                setattr(var1d, attrname, attrval)
                
        vcontain.append(var1d)
        
        file_nc.sync()
    file_nc.close()

    

#  this function is used to write var to netcdf file.

def netCDF_var_write(filename,dimNames,varName, varType, varData, varattr=None):
    file_nc=snf.Dataset(filename, 'a')
    ndim=size(dimNames)
    # print filename
    #  print dimNames
    
    if (ndim>1):
        dim_nd=tuple(dimNames)
    else:
        dim_nd=(dimNames[0],)
    # print dim_nd
    # print 'varName', varName
    
    if ('_cp' in varName):
        varName=varName.replace('_cp', '')
        cdf_var=file_nc.createVariable(varName, varType, dim_nd, zlib=True , complevel=1)
    else:
        cdf_var=file_nc.createVariable(varName, varType, dim_nd)
   
    # cdf_var.zlib=True
    
    # var=array(varData)
    
    idx=slice(None)
    nsizes=shape(varData)
    cdf_var[idx]=varData[idx]
    
    setattr(cdf_var, '_fill_value', -999.0)
    if (varattr<>None):
        for attrname in varattr:
            attrval=varattr[attrname]
            setattr(cdf_var, attrname, attrval)
    
    
    file_nc.close()



if (__name__=="__main__"):
    # define the netcdf file
    filename="test.nc"
    
    dimNames=list()
    dimNames.append('profile')
    dimNames.append('level')

    dimTypes=list()
    dimTypes.append('i')
    dimTypes.append('f')

    prof_Nos=arange(30)
    std_pres=arange(-3.0, 2.01, 1./6.0)
    
    dimVars=list()
    dimVars.append(prof_Nos)
    dimVars.append(std_pres)
    
    netCDF_def_dims(filename,dimNames,dimTypes, dimVars)

    t=zeros([len(prof_Nos), len(std_pres)], Float)
    varName='Temperature'
    varType='f'
    dimNames=list()
    dimNames.append('profile')
    dimNames.append('level')
    varData=t
    
    netCDF_var_write(filename,dimNames,varName, varType, varData)



    


    

    
    
        
        
        
        
        
    
