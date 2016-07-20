addpath('/data/nsoontie/t_tide')
addpath('/data/nsoontie/MEOPAR/analysis/Nancy/currents/t_tide_analysis')

%load data
filename='/ocean/nsoontie/MEOPAR/SalishSea/results/other_mixing/biharm_1e6_tra5e5/PointAtkinson_10.nc';
ncid = netcdf.open(filename);
ssh = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'sossheig'));
time_counter = netcdf.getVar(ncid, netcdf.inqVarID(ncid,'time_counter'));
netcdf.close(ncid);

%time
ref_time=[1900,1,1];
mtimes = time_to_mtime(time_counter, ref_time, 's'); 
t0=721;
start=mtimes(t0);
interval=1/6;

%latitude for nodal corrections (approximate)
lat=49.3304;

%inference - Susan's notebook (TidalEvaluationTake2.ipynb)
%Eyeball of plot from cell 14
infername=['P1';'K2'];
inferfrom=['K1';'S2'];
infamp=[.31;.27];
infphase=[-3;-.5];

%tide fit - without inferece
outfile = 'biharm_1e6_tra5e5_tides';
tide_struc=t_tide(ssh(t0:end),'start time',start,'latitude',lat,'interval',interval,'output',outfile);
%tide fit - with inference
outfile = 'biharm_1e6_tra5e5_inference';
tide_struc_inf=t_tide(ssh(t0:end),'start time',start,'latitude',lat,'interval',interval,'output',outfile, 'inference',infername, inferfrom, infamp,infphase);