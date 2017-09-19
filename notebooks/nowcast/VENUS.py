# Script to plot VENUS comparisons

import matplotlib.pyplot as plt
import numpy as np
import netCDF4 as nc
import datetime
from dateutil import tz
import os
import pandas as pd
import xarray as xr

from salishsea_tools import (
    geo_tools,
    places,
    psu_tools,
    teos_tools,
    data_tools,
    tidetools,
)

from nowcast import analyze
from nowcast.figures import shared


def get_onc_TS_time_series(station):
    """Grab the ONC temperature and salinity time series for
       station between dates  t_o and t_f.
       Return results as separate temperature and salinty data frames.
        reults are from erdap"""
    code = 'ubcONC{}CTD15mV1'.format(places.PLACES[station]['ONC stationCode'])
    url = 'https://salishsea.eos.ubc.ca/erddap/tabledap/{}'.format(code)
    print(url)
    data = nc.Dataset(url)
    return data


def get_model_time_series(station, fnames, grid_B, mesh_mask, nemo_36=True):
    """Retrieve the density, salinity and temperature time series at a station.
    Time series is created from files listed in fnames"""
    if nemo_36:
        depth_var = 'gdept_0'
        depth_var_w = 'gdepw_0'
    else:
        depth_var = 'gdept'
        depth_var_w = 'gdepw'
    # station info
    lon = places.PLACES[station]['lon lat'][0]
    lat = places.PLACES[station]['lon lat'][1]
    depth = places.PLACES[station]['depth']
    # model corresponding locations and variables
    bathy, X, Y = tidetools.get_bathy_data(grid_B)
    j, i = geo_tools.find_closest_model_point(lon, lat,
                                              X, Y,
                                              land_mask=bathy.mask)
    model_depths = mesh_mask.variables[depth_var][0, :, j, i]
    tmask = mesh_mask.variables['tmask'][0, :, j, i]
    wdeps = mesh_mask.variables[depth_var_w][0, :, j, i]
    sal, time = analyze.combine_files(fnames, 'vosaline', 'None', j, i)
    temp, time = analyze.combine_files(fnames, 'votemper', 'None', j, i)
    # interpolate:
    sal_interp = np.array(
        [shared.interpolate_tracer_to_depths(
            sal[d, :], model_depths, depth, tmask, wdeps)
            for d in range(sal.shape[0])])
    temp_interp = np.array(
        [shared.interpolate_tracer_to_depths(
            temp[d, :], model_depths, depth, tmask, wdeps)
            for d in range(temp.shape[0])])
    # convert to psu for using density function
    return sal_interp, temp_interp, time


def plot_station(stations, runs, t_o, t_f):

    times = {'nowcast': {}, 'nowcast-green': {}}
    sals = {'nowcast': {}, 'nowcast-green': {}}
    temps = {'nowcast': {}, 'nowcast-green': {}}
    for sim in ['nowcast-green']:
        print(sim)
        for station in stations:
            print(station)
            sals[sim][station], temps[sim][station], times[sim][station] = \
                get_model_time_series(station, runs[sim]['fnames'],
                                      runs[sim]['grid'],
                                      runs[sim]['mesh'],
                                      nemo_36=runs[sim]['nemo36'])

    fig, axs = plt.subplots(2, 4, figsize=(25, 10), sharex=True)
    names = ['Salinty [g/kg]', 'Temperature [C]']
    titles = ['salinity', 'temperature']
    ticks = [[28, 32], [7, 12]]
    cols = ['g']
    for i, station in enumerate(stations):
        axc = axs[:, i]
        obs = get_onc_TS_time_series(station)
        for sim, col in zip(['nowcast-green'], cols):
            variables = [sals[sim], temps[sim]]
            t = times[sim]
            for var, name, title, ax, tick in zip(variables, names, titles,
                                                  axc, ticks):
                if sim == 'nowcast-green':  # only plot obs once
                    var_obs = obs.variables['s.{}'.format(title)][:]
                    time_obs = obs.variables['s.time']
                    dates_obs = nc.num2date(time_obs[:], time_obs.units)
                    obs_d = pd.DataFrame({'time': dates_obs, title: var_obs})
                    date_index = pd.DatetimeIndex(obs_d['time'])
                    obs_d['date_index'] = date_index
                    obs_d.set_index('date_index', inplace=True)
                    obs_day = obs_d.resample('D', how='mean')
                    ax.plot(obs_day.index, obs_day[title],
                            'k', label='obs'.format(station), lw=2)
                ax.plot(np.array(t[station]), np.array(var[station]),
                        c=col, label=sim, lw=2)
                ax.set_ylabel('Daily averaged {}'.format(name))
                ax.set_title('{} - {} m'.format(station,
                                                places.PLACES[station]['depth']))
                ax.set_ylim(tick)
    for ax in axs.flatten():
        ax.grid()
        ax.set_xlim([t_o, t_f])
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
    for ax in axs[:, -1]:
        ax.legend(loc=(1, 0.25))
    fig.autofmt_xdate()
    plt.show()
    fig.savefig('VENUS.png')


t_o = datetime.datetime(2014, 9, 12)
t_f = datetime.datetime(2017, 9, 11)
fnames = analyze.get_filenames(t_o, t_f, '1d', 'grid_T',
                               '/results/SalishSea/nowcast-green/')
grid_B = nc.Dataset(
    '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathymetry_201702.nc')
mesh_mask = nc.Dataset(
    '/data/nsoontie/MEOPAR/NEMO-forcing/grid/mesh_mask201702.nc')

runs = {'nowcast-green': {'grid': grid_B,
                          'mesh': mesh_mask,
                          'fnames': fnames,
                          'nemo36': True}}
stations = ['East node', 'Central node', 'Delta DDL node', 'Delta BBL node']
plot_station(stations, runs, t_o, t_f)
