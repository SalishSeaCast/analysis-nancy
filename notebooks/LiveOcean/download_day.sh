# Script to transfer a LiveOcean time series to /ocean
# Download's all files for the specified run day (72 hours).
# Uses wget to download files and also UBC_subdomain.py to extract subdomain
# Original Live Ocean files (100mb each) are deleted
# Example usage: bash download_day.sh 2016-06-09 DEST
# downloads 72 hours for a Live Ocean run that began on June 9, 2016. Places the
# files in a directory DEST/20160609/

DEST=$2
SOURCE=https://pm2.blob.core.windows.net/f
TOOLS_PATH=/data/nsoontie/MEOPAR/tools/SalishSeaTools/salishsea_tools

d=$(date -I -d "$1") || exit -1

#create new directory
subdir=`date --date="$d" '+%Y%m%d'`
mkdir $DEST/$subdir
for f in $(seq -f %04g 2 73); do
   fname=$SOURCE$subdir/ocean_his_$f.nc
   fname_save=$DEST/$subdir/ocean_his_$f.nc
   wget -O $fname_save $fname
   python $TOOLS_PATH/UBC_subdomain.py $fname_save
   rm -f $fname_save
done
# compression
for f in $DEST/$subdir/*.nc; do
    ncks -4 -L4 -O $f $f
done