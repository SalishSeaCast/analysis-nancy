# Python script for extracting a subset of Live Ocean results
# ---------------------------------------------------------------------------
# Usage
#
# From command line:
# python UBC_subdomain.py filename1 filename2 filename3 ...
#
# Inside python:
# import UBC_subdomain
# UBC_subdomain.get_UBC_subdomain([filename1, filename2, filename3,...])
# ----------------------------------------------------------------------------
# Description
#
# Creates new netCDF files that store a subdomain and subset of variables
# for UBC users (S. Allen's group).
# New file names are derived from the original file name with '_UBC' suffix.
# For example: ocean_his_0002.nc becomes ocean_his_0002_UBC.nc
# ----------------------------------------------------------------------------
# Written by
# Nancy Soontiens 2016
# nsoontie@eos.ubc.ca

import sys
import netCDF4 as nc

# Bounds of subdomain
XBS = [55, 80]  # x-limits
YBS = [295, 325]  # y-limits
# Variables to copy
VAR_LIST = ['salt', 'temp', 'h', 'lon_rho', 'lat_rho', 'mask_rho', 'pn', 'pm',
            's_rho', 'hc', 'Cs_r', 'Vtransform', 'zeta', 'ocean_time']
# Dimensions to copy
DIM_LIST = ['xi_rho', 'eta_rho', 'N', 's_rho', 'ocean_time']


def main():
    f_list = sys.argv[1:]
    get_UBC_subdomain(f_list)


def get_UBC_subdomain(f_list):
    """Create subdomain files for all netCDF files in f_list """
    for fname in f_list:
        fnew = '{}_UBC.nc'.format(fname.split('.nc', 1)[0])
        with nc.Dataset(fname) as G, nc.Dataset(fnew, 'w') as Gnew:
            _copy_netCDF_subdomain(G, Gnew, XBS, YBS, VAR_LIST, DIM_LIST)


def _copy_netCDF_subdomain(oldfile, newfile, xbounds, ybounds,
                           var_list, dim_list):
    """Copy variables in var_list in subdomain [xbounds, ybounds] from
       oldfile to newfile. Also copies dimensions in dim_list and
       all global attributes.
    """
    _copy_dimensions(oldfile, newfile, dim_list, xbounds, ybounds)
    _copy_variables(oldfile, newfile, var_list, xbounds, ybounds)
    # copy global attributes
    newfile.setncatts(
        {att: oldfile.getncattr(att) for att in oldfile.ncattrs()}
        )


def _copy_dimensions(oldfile, newfile, dim_list, xbounds, ybounds):
    """ Copy the dimensions in dims_list from oldfile to newfile.
        Dimensions of eta_rho, xi_rho are determined by limits of
        ybounds, xbounds. """
    for dimname in dim_list:
        dim = oldfile.dimensions[dimname]
        if dimname == 'eta_rho':
            newfile.createDimension(dimname, size=ybounds[1]-ybounds[0]+1)
        elif dimname == 'xi_rho':
            newfile.createDimension(dimname, size=xbounds[1]-xbounds[0]+1)
        elif dimname == 'ocean_time':
            newfile.createDimension(dimname, size=0)
        else:
            newfile.createDimension(dimname, size=dim.__len__())


def _copy_variables(oldfile, newfile, var_list, xbounds, ybounds):
    """Copy variables in var_list from oldfile to newfile for subdomain
        [xbounds, ybounds]"""
    for varname in var_list:
        var = oldfile.variables[varname]
        dims = var.dimensions
        newvar = newfile.createVariable(varname, var.datatype, dims)
        # copy variable attributes
        newvar.setncatts({att: var.getncattr(att) for att in var.ncattrs()})
        # fill data
        if 'eta_rho' in dims or 'xi_rho' in dims:
            newvar[:] = var[...,
                            ybounds[0]:ybounds[1]+1,
                            xbounds[0]:xbounds[1]+1]
        else:
            newvar[:] = var[:]


if __name__ == '__main__':
    main()
