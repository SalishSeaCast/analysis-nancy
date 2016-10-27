# Script download and generate boundary files from today's Live Ocean results.
# For use in cron

DATE=`date +%Y-%m-%d`
DEST=/results/forcing/LiveOcean/downloaded/
bash download_day.sh $DATE $DEST

/home/nsoontie/anaconda3/envs/analysis/bin/python LiveOcean_BCs.py $DATE
