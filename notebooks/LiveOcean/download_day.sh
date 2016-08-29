# Script to transfer a LiveOcean time series to /ocean
# Download's all files for the specified run day (72 hours).
# Uses wget to download files and also UBC_subdomain.py to extract subdomain
# Original Live Ocean files (100mb each) are deleted
# Example usage: bash download_runday.sh 2016-06-09 DEST
# downloads 72 hours for a Live Ocean run that began on June 9, 2016. Places the
# files in a directory DEST/20160609/

DEST=$2
SOURCE=https://pm2.blob.core.windows.net/f

d=$(date -I -d "$1") || exit -1

#create new directory
subdir=`date --date="$d" '+%Y%m%d'`
mkdir $DEST/$subdir
for f in $(seq -f %04g 2 73); do
   fname=$SOURCE$subdir/ocean_his_$f.nc
   fname_save=$DEST/$subdir/ocean_his_$f.nc
   wget -O $fname_save $fname
   python UBC_subdomain.py $fname_save
   rm -f $fname_save
done
