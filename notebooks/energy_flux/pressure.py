# A module to calculate various pressure terms for NEMO

import numpy as np


def hydrostatic_pressure(rho, e3t, gdept, tmask, return_masked=True):
    """Vertically integrate hydrostatic equation to calculate pressure.
    dp/dz = -rho(z)*g
    Should use time-dependent scale factors and depths.

    :arg rho: density on T-grid (kg/m^3). Dimensions: (time, depth, y, x)
    :type rho: numpy array

    :arg e3t: vertical scale factors on T-grid (m).
              Dimensions: (time, depth, y, x)
    :type e3t: numpy array

    :type gdept: depths on T-grid (m). Dimensions: (time, depth, y, x)
    :arg gdept: numpy array.

    :arg tmask: T-grid mask. Dimensions: (time, depth, y, x) or (depth, y, x)
    :type tmask: numpy array

    :arg return_masked: specifies that pressure should be returned as masked
                        array
    :type return_masked: boolean

    :returns: pressure in Pascals"""
    g = 9.81  # Acceleration due to gravity (m/s^2)

    # integrate density to get pressure
    p = np.cumsum(g*rho*e3t*tmask, axis=1)
    # Attempt to approximate p(z=0)=0.
    p = p - np.expand_dims(g*rho[:, 0, ...]*gdept[:, 0, ...], axis=1)
    if return_masked:
        p = np.ma.array(p, mask=np.ones(p.shape) - tmask)
    return p


def depth_average_pressure(p, e3t, tmask):
    """Calculate the depth averaged pressure.
    Should use time-dependent scale factors.

    :arg p: pressure on T-grid. Dimensions: (time, depth, y, x)
    :type p: numpy array

    :arg e3t: vertical scale factors on T-grid (m).
              Dimensions: (time, depth, y, x)
    :type e3t: numpy array

    :arg tmask: T-grid mask. Dimensions: (time, depth, y, x) or (depth, y, x)
    :type tmask: numpy array

    :returns: depth averaged pressure in same units as input pressure.
              Dimensions: (time, y, x)"""

    H = np.sum(e3t*tmask, axis=1)
    p_integral = np.sum(p*e3t*tmask, axis=1)

    p_davg = p_integral/H
    p_davg = np.nan_to_num(p_davg)

    return p_davg


def internal_tide_pressure(p, e3t, tmask, return_masked=True):
    """Calculate the internal tide pressure.
    p_it = p - p_depthaveraged
    Should use time-dependent scale factors.

    :arg p: pressure on T-grid. Dimensions: (time, depth, y, x)
    :type p: numpy array

    :arg e3t: vertical scale factors on T-grid (m).
              Dimensions: (time, depth, y, x)
    :type e3t: numpy array

    :arg tmask: T-grid mask. Dimensions: (time, depth, y, x) or (depth, y, x)
    :type tmask: numpy array

    :arg return_masked: specifies that pressure should be returned as masked
                        array
    :type return_masked: boolean

    :returns: internal pressure in same units as input pressure.
              Dimensions: (time, depth, y, x)"""

    p_davg = depth_average_pressure(p, e3t, tmask)
    p_it = p - np.exand_dims(p_davg, axis=1)
    if return_masked:
        p_it = np.ma.array(p_it, mask=np.ones(p_it.shape) - tmask)
    return p_it
