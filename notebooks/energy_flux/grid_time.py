# Functions for calculating time-dependent scale factors and depth in NEMO.
# NKS nsoontie@eos.ubc.ca 08-2016


import numpy as np


def calculate_v(e3t0, tmask):
    """
    Calculate the v correction factor for variable volume in NEMO.
    e3t0 and tmask must be the same shape.
    See NEMO vvl manual appendix A.1 for details.

    :arg e3t0: initial vertical scale factors on T-grid
               Dimensions: (depth, y, x)
    :type e3t0: numpy array

    :arg tmask: T-grid mask
                Dimensions: (depth, y, x)
    :type tmask: numpy array

    :returns: The v correction factor, a numpy array
              Dimensions: (y, x)

    """
    vn = 0
    for k in np.arange(e3t0.shape[0]):
        sum1 = 0
        for n in np.arange(k, e3t0.shape[0]):
            sum1 = sum1 + e3t0[n, ...]*tmask[n, ...]
        vn = vn + e3t0[k, :, :]*sum1*tmask[k, ...]
    return vn


def calculate_adjustment_factor(e3t0, tmask, v, ssh):
    """
    Calculate the adjustment factor for variable volume in NEMO.
    See NEMO vvl manual appendix A.1 for details.

    :arg e3t0: Initial vertical scale factors on T-grid
               Dimensions: (depth, y, x)
    :type e3t0: numpy array

    :arg tmask: T-grid mask.
                Dimensions: (depth, y, x)
    :type tmask: numpy array

    :arg v: v correction factor.
            Dimensions: (y, x)
    :type v: numpy array

    :arg ssh: The model sea surface height
              Dimensions: (time, depth, y, x)
    :type ssh: numpy array

    :returns: The adjustment factor, a numpy array
              Dimensions (time, depth, y, x)
    """
    # Define shape of adj
    shape = list(e3t0.shape[:])
    shape.insert(0, ssh.shape[0])
    adj = np.zeros(shape)

    for k in np.arange(e3t0.shape[0]):
        sum1 = 0
        for n in np.arange(k, e3t0.shape[0]):
            sum1 = sum1 + e3t0[n, ...]*tmask[n, ...]
        adj[:, k, ...] = (1 + ssh/v*sum1)
    inds = np.where(np.isnan(adj))
    adj[inds] = 1  # Turn nans into ones

    return adj


def calculate_vertical_grids(e3t0, tmask, ssh):
    """
    Calcuate the time dependent vertical grids and scale factors for
    variable volume in NEMO.
    See NEMO vvl manual appendix A.1 for details.

    :arg e3t0: Initial vertical scale factors on T-grid
               Dimensions: (depth, y, x).
    :type e3t0: numpy array

    :arg tmask: T-grid mask
                Dimensions: (depth, y, x)
    :type tmask: numpy array

    :arg ssh: Model sea surface height
              Dimensions: (time, depth, y, x)
    :type ssh: numpy array

    :returns: e3t_t, e3t_3, gdept_t, gdept_w
    The time dependent vertical scale factors on t and w grids and depths
    on t and w grids.
    Dimensions: (time, depth, y, x)
    """

    # adjustment factors
    vn = calculate_v(e3t0, tmask)
    adj = calculate_adjustment_factor(e3t0, tmask, vn, ssh)
    # scale factors
    e3t_t = e3t0*adj
    # initialize for k=0
    e3w_t = np.copy(e3t_t)
    # overwrite k>0
    e3w_t[:, 1:, ...] = 0.5*(e3t_t[:, 1:, ...] + e3t_t[:, 0:-1, ...])
    # depths
    # initialize for k=0
    gdept_t = 0.5*e3t_t
    gdepw_t = np.zeros(gdept_t.shape)
    for k in np.arange(1, gdept_t.shape[1]):
        # overwrite k>0
        gdept_t[:, k, ...] = gdept_t[:, k-1, ...] + e3w_t[:, k, ...]
        gdepw_t[:, k, ...] = gdepw_t[:, k-1, ...] + e3t_t[:, k-1, ...]

    return e3t_t, e3w_t, gdept_t, gdepw_t
