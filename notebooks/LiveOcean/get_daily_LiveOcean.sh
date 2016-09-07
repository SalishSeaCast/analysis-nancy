# Script download and generate boundary files from today's Live Ocean results.
# For use in cron

DATE=`date +%Y-%m-%d`
DEST=/ocean/nsoontie/MEOPAR/LiveOcean/subdomain_files
bash download_day.sh $DATE $DEST

/home/nsoontie/anaconda3/envs/analysis/bin/python LiveOcean_BCs.py $DATE
SAVEDIR=/ocean/nsoontie/MEOPAR/LiveOcean/boundary_files/$DATE
for file in $SAVEDIR/*.nc; do
    ncks -O --mk_rec_dmn=time_counter $file $file
done