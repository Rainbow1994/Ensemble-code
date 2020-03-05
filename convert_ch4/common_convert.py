import geo_constant as gc
import gp_fields as gf
from scipy import *
from scipy.integrate import simps 

def get_tc_kg_from_vmr(p, vmr):
    """ get the column volume of the molecules
    Arguments:
    p :  pressure in hPa
    vmr : volume mixing ratio
    return : tc in kg/m2
    """
    tc=simps(vmr[::-1], p[::-1])
    tc=100*tc  #  change to  Pa
    tc=tc/gc.g0
    return tc
def get_column_ratio(tc, ps):
    """ get the column volume of the molecules
    Arguments:
    ps :  surface pressure in hPa
    tc : column volume in kg/m2
    return : col_ratio
    """
    col_ratio=tc/(100*ps/gc.g0)
    return col_ratio


def mass_to_number(mass, molew):
    """ get the column volume of the molecules
    Arguments:
    mass :  air mass in kg
    molew:  molecular weight in g/mole
    return :number of molecules
    """
    molen=gc.An*gc.mass*1.0e3/molew

