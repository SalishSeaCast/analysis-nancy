# Create the JuandeDucaMouth.dat file from Rob's IOS and NOAA data
# Looks for data points close to the mouth of JdF.

import ACTDR
import netCDF4 as nc

# Load IOS and NOAA data
ACTDR.load_ios()
ACTDR.load_noaa()

# Filter year
ACTDR.filter_year(2003)

# Filter data without Temperature and Salinity keys
ACTDR.filter_keys()

# Filter lon/lats.
# Load SalishSea model
b = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/bathy_meter_SalishSea2.nc'
grid_B = nc.Dataset(b)
bathy = grid_B.variables['Bathymetry'][:]
lat = grid_B.variables['nav_lat'][:]
lon = grid_B.variables['nav_lon'][:]
# min/max lon and lat along JdF boundary
min_lon = lon[380:470, 0].min()
max_lon = lon[380:470, 0].max()
min_lat = lat[380:470, 0].min()
max_lat = lat[380:470, 0].max()
# remove indices outside of range
rm_ind = []
# rm_ind contains the indices to remove
# loop through all casts
for ii, cast in enumerate(ACTDR.CTD_DAT):
    # see if cast is outside of my region region
    if (cast['Latitude'] > max_lat or cast['Latitude'] < min_lat or
       cast['Longitude'] > max_lon or cast['Longitude'] < min_lon):
        rm_ind.append(ii)  # append to the remove list if outside

# loop through the removed indices list
for ii in rm_ind[::-1]:
    del ACTDR.CTD_DAT[ii]  # delete said index

# let the user know the new number of available casts

print '> ', len(ACTDR.CTD_DAT), ' casts'

# save new database
ACTDR.save_dat('JuandeFucaMouth.dat')
