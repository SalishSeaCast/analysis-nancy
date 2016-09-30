addpath('/data/nsoontie/t_tide')

files = cell(1);
outs = cell(1);
depthfile = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/mesh_mask_SalishSea2.nc';

%files{1} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/BP_currents_20160622_20160825.nc';
files{1} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/NSoG_currents_20141126_20150426.nc';
%files{3} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/VictoriaSill_currents_20141126_20150426.nc';
%files{4} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/JuandeFuca_currents_20141126_20150426.nc';

%outs{1} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/BP_region_surface_20160622_20160825.mat';
outs{1} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/CODAR/NSoG_region_surface_20141126_20150426.mat';
%outs{3} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/VictoriaSill_baroclinic_depav_20141126_20150426_masked.mat';
%outs{4} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/JuandeFuca_baroclinic_depav_20141126_20150426_masked.mat';

%% Bathy mods
% files{1} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2/CODAR_all.nc';
% files{2} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2_nowinds/CODAR_all.nc';
% files{3} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy6/CODAR_all.nc';
% files{4} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy9/CODAR_all.nc';
% files{5} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy10/CODAR_all.nc';
% 
% depthfiles{1} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2/mesh_mask.nc';
% depthfiles{2} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2_nowinds/mesh_mask.nc';
% depthfiles{3} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy6/mesh_mask.nc';
% depthfiles{4} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy9/mesh_mask.nc';
% depthfiles{5} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy10/mesh_mask.nc';
% 
% outs{1} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2/baroclinic_tides_masked';
% outs{2} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy2_nowinds/baroclinic_tides_masked';
% outs{3} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy6/baroclinic_tides_masked';
% outs{4} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy9/baroclinic_tides_masked';
% outs{5} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy10/baroclinic_tides_masked';

%% Nemo 36

% files{1} = '/ocean/sallen/allen/research/MEOPAR/myResults/NEMO36_Tides/TS4/CODAR.nc';
% outs{1} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/TS4/baroclinic_tides_masked';
% depthfiles{1} = '/data/nsoontie/MEOPAR/SalishSea/results/tides/bathymods/bathy6/mesh_mask.nc';

%% 
%%% Change these values when doing bathy mod!!!!
t0=1;
ref_time = [2014 09, 10];
%ref_time = [2003,4,21];
%ref_time = [1900, 01, 01];
time_units='h';
use_mask=1
%%%

for i=1:length(files)
    filename = files{i}
    %depthfile = depthfiles{i}
    outfile = outs{i}
    area_surface_tides(filename, outfile, t0, ref_time, time_units)
end
