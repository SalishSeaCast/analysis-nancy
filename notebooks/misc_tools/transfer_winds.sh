# Script to transfer operational winds from /results to orcinus
# Uses scp to transfer the files
# Usage: bash transfer_winds.sh 2016-07-27 2016-08-21
# transfers weather files in interval [July 27, 2016, August 21, 2016)

DEST=/home/sallen/MEOPAR/GEM2.5/ops/NEMO-atmos/
SOURCE=/results/forcing/atmospheric/GEM2.5/operational/

#start and end dates of the transfer period
start=$1
end=$2

d=$(date -I -d "$start") || exit -1
end_date=$(date -I -d "$end") || exit -1

while [ "$d" != "$end_date" ]; do
   fname=`date --date="$d" '+ops_y%Ym%md%d.nc'`
   echo $fname
   scp $SOURCE$fname orcinus:$DEST.
   ssh orcinus "chgrp wg-moad $DEST$fname"
   ssh orcinus "chmod 664 $DEST$fname"
   d=$(date -I -d "$d + 1 day")
done