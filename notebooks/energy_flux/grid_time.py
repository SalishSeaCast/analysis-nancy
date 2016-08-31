# Functions for calculating time-dependent scale factors and depth in NEMO.
# NKS nsoontie@eos.ubc.ca 08-2016


import numpy as np


def calculate_mu(e3t0, tmask):
    """Calculate the mu correction factor for variable volume in NEMO.
    e3t0 and tmask must be the same shape.
    See NEMO vvl manual appendix A.1 for details.

    :arg e3t0: initial vertical scale factors on T-grid.
               Dimensions: (depth, y, x).
    :type e3t0: numpy array

    :arg tmask: T-grid mask. Dimensions: (depth, y, x)
    :type tmask: numpy array

    :returns: the mu correction factor with dimensions (depth, y, x)

    """
    # Iterate over k to find v and inner sum
    vn = 0
    sum_matrix = np.zeros(e3t0.shape)
    for k in np.arange(e3t0.shape[0]):
        inner_sum = 0
        for n in np.arange(k, e3t0.shape[0]):
            inner_sum = inner_sum + e3t0[n, ...]*tmask[n, ...]
        sum_matrix[k, ...] = inner_sum
        vn = vn + e3t0[k, ...]*inner_sum*tmask[k, ...]

    mu = sum_matrix/vn
    mu = np.nan_to_num(mu)  # turn nans to zeros
    return mu


def calculate_adjustment_factor(mu, ssh):
    """Calculate the time=dependent adjustment factor for variable volume in
    NEMO. adj = (1+ssh*mu) and e3t_t = e3t_0*adj
    See NEMO vvl manual appendix A.1 for details.

    :arg mu: mu correction factor. Dimension: (depth, y, x)
    :type mu: numpy array

    :arg ssh: the model sea surface height. Dimensions: (time, y, x)
    :type ssh: numpy array

    :returns: the adjustment factor with dimensions (time, depth, y, x)
    """
    # Give ssh a depth dimension
    ssh = np.expand_dims(ssh, axis=1)
    adj = (1 + ssh*mu)

    return adj


def calculate_vertical_grids(e3t0, tmask, ssh):
    """ Calculate the time dependent vertical grids and scale factors for
    variable volume in NEMO. See NEMO vvl manual appendix A.1 for details.

    :arg e3t0: initial vertical scale factors on T-grid.
               Dimensions: (depth, y, x).
    :type e3t0: numpy array

    :arg tmask: T-grid mask. Dimensions: (depth, y, x)
    :type tmask: numpy array

    :arg ssh: the model sea surface height. Dimensions: (time, depth, y, x)
    :type ssh: numpy array

    :returns: e3t_t, e3t_3, gdept_t, gdept_w
    The time dependent vertical scale factors on t and w grids and depths on
    t and w grids.
    Dimensions: (time, depth, y, x)
    """
    # adjustment factors
    mu = calculate_mu(e3t0, tmask)
    adj = calculate_adjustment_factor(mu, ssh)
    # scale factors
    e3t_t = e3t0*adj
    # intiliaize for k=0
    e3w_t = np.copy(e3t_t)
    # overwrite k>0
    e3w_t[:, 1:, ...] = 0.5*(e3t_t[:, 1:, ...] + e3t_t[:, 0:-1, ...])
    # depths
    # initialize for k=0
    gdept_t = 0.5*e3t_t
    gdepw_t = np.zeros(gdept_t.shape)
    # overwrite k>0
    for k in np.arange(1, gdept_t.shape[1]):
        gdept_t[:, k, ...] = gdept_t[:, k-1, ...] + e3w_t[:, k, ...]
        gdepw_t[:, k, ...] = gdepw_t[:, k-1, ...] + e3t_t[:, k-1, ...]

    return e3t_t, e3w_t, gdept_t, gdepw_t
