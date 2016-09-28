# A module to calculate conversion and useful values for energy flux.
# Based on Kelly et al 2010.


import numpy as np
import pressure

from salishsea_tools import grid_tools, psu_tools


def bathymetry_gradient(bathy, e1u, e2v):
    """Calculate the bathymetry gradient, H_x and H_y. Not that these are the
    gradients on the U-grid (H_x) and V-grid (H_y).

    :arg bathy: bathymetry array. Dimensions: (y, x)
    :type bathy: numpy array

    :arg mesh_mask: netCDF handle that contains mesh mask information
    :type mesh_mask: netCDF4 Dataset

    :returns: the x-derivative and y-derivative of the bathymetry.
    """

    diff_x = bathy[:, 1:] - bathy[:, :-1]
    diff_y = bathy[1:, :] - bathy[:-1, :]
    # pad with zeros in first row
    diff_x = np.concatenate([diff_x, np.zeros((bathy.shape[0], 1))], axis=1)
    # pad with zeros in first column
    diff_y = np.concatenate([diff_y, np.zeros((1, bathy.shape[1]))], axis=0)

    hx = diff_x/e1u
    hy = diff_y/e2v

    return hx, hy


def depth_average(var, grid, mask):
    """Calculate the depth average of a variable.

    :arg var: The variable to be depth-averaged.
              Dimensions: (time, depth, y, x)
    :type var: numpy array

    :arg grid: the vertical scale factors. Dimensions: (time, depth, y, x)
    :type grid: numpy array

    :arg mask: the grid's mask. Dimensions: (depth, y, x)
    :type mask: numpy array

    :returns: the depth averaged variable. Dimensions: (time, y, x)
    """
    integral = np.sum(var*grid*mask, axis=1)
    H = np.sum(grid*mask, axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        one_over_H = 1 / H
    one_over_H = np.nan_to_num(one_over_H)
    return integral*one_over_H


def depth_averaged_u(u, ssh, grids):
    grids_u = grid_tools.time_dependent_grid_U(grids['e3u_0'][0, ...],
                                               grids['e1u'][0, ...],
                                               grids['e2u'][0, ...],
                                               grids['e1t'][0, ...],
                                               grids['e2t'][0, ...],
                                               grids['umask'][0, ...],
                                               ssh[:],
                                               {'e3u_0': grids['e3u_0'][0, ...]})

    u_depav = depth_average(u, grids_u['e3u_t'],
                            grids['umask'][0, :, :, :])

    return u_depav


def depth_averaged_v(v, ssh, grids):
    grids_v = grid_tools.time_dependent_grid_V(grids['e3v_0'][0, ...],
                                               grids['e1v'][0, ...],
                                               grids['e2v'][0, ...],
                                               grids['e1t'][0, ...],
                                               grids['e2t'][0, ...],
                                               grids['vmask'][0, ...],
                                               ssh[:],
                                               {'e3v_0': grids['e3v_0'][0, ...]})

    v_depav = depth_average(v, grids_v['e3v_t'],
                            grids['vmask'][0, :, :, :])

    return v_depav


def load_grids_subdomain(mesh_mask, jss, iss,
                         vs=['e3t', 'e2t', 'e1t', 'tmask', 'gdept',
                             'e3w', 'gdepw',
                             'e3u', 'e2u', 'e1u', 'umask', 'gdepu',
                             'e3v', 'e2v', 'e1v', 'vmask', 'gdepv']):
    grids = {}
    for v in vs:
        grids[v] = mesh_mask.variables[v][...,
                                          jss[0]:jss[-1]+1,
                                          iss[0]:iss[-1]+1]
    # rename vertical stuff with _0
    for v in ['gdept', 'gdepw', 'gdepu', 'gdepv',
              'e3t', 'e3w', 'e3u', 'e3v']:
        if v in vs:
            new_key = v + '_0'
            grids[new_key] = grids.pop(v)
    return grids


def barotropic_w(u, v, ssh, bathy, grids):

    hx, hy = bathymetry_gradient(bathy, grids['e1u'], grids['e2v'])

    u_depav = depth_averaged_u(u, ssh, grids)
    v_depav = depth_averaged_v(v, ssh, grids)

    w_bar = -u_depav * hx - v_depav * hy

    return w_bar


def conversion_CT(w_bar, p_it,  mbathy):

    bottom_p = np.zeros(w_bar.shape)
    for j in np.arange(bottom_p.shape[-2]):
        for i in np.arange(bottom_p.shape[-1]):
            level = mbathy[j, i]
            bottom_p[:, j, i] = p_it[:, level, j, i]

    return w_bar*bottom_p
