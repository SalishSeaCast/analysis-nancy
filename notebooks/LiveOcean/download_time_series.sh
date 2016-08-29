# Script to transfer a LiveOcean time series to /ocean
# Only the nowcast files are downloaded. 
# Uses wget to download files and also UBC_subdomain.py to extract subdomain
# Original Live Ocean files (100mb each) are deleted
# Example usage: bash download_daily.sh 2016-06-09 2016-06-20
# downloads 24 hours for each day in [June 9, 2016, June 20, 2016)

DEST=/ocean/nsoontie/MEOPAR/LiveOcean/
SOURCE=https://pm2.blob.core.windows.net/f

d=$(date -I -d "$1") || exit -1
end_date=$(date -I -d "$2") || exit -1

while [ "$d" != "$end_date" ]; do
    #create new directory
    subdir=`date --date="$d" '+%Y%m%d'`
    mkdir $DEST$subdir
    for f in $(seq -f %04g 2 25); do
       fname=$SOURCE$subdir/ocean_his_$f.nc
       fname_save=$DEST$subdir/ocean_his_$f.nc
        wget -O $fname_save $fname
       python UBC_subdomain.py $fname_save
       rm -f $fname_save
    done
    d=$(date -I -d "$d + 1 day")
done
