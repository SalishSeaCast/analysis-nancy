addpath('/data/nsoontie/t_tide')

files = cell(1);
outs = cell(1);
depthfile = '/data/nsoontie/MEOPAR/NEMO-forcing/grid/mesh_mask_SalishSea2.nc';

files{1} ='/ocean/nsoontie/MEOPAR/TidalEllipseData/ModelTimeSeries/CODAR_TS_20141126_20150426.nc';
outs{1} = '/ocean/nsoontie/MEOPAR/TidalEllipseData/CODAR/CODAR_region_20141126_20150426';

%% 
%%% Change these values when doing bathy mod!!!!
t0=1;
ref_time = [2014 09, 10];
time_units='h';
%%%

for i=1:length(files)
    filename = files{i};
    %depthfile = depthfiles{i}
    outfile = outs{i};
    area_wN2_analysis_kunze(filename, outfile, depthfile, t0, ref_time, time_units)
end
