# Script download and generate boundary files from today's Live Ocean results.
# For use in cron

DATE=`date +%Y-%m-%d`
DEST=/results/forcing/LiveOcean/downloaded/
TOOLS_PATH=/data/nsoontie/MEOPAR/tools/SalishSeaTools/salishsea_tools
bash download_day.sh $DATE $DEST

/home/nsoontie/anaconda3/envs/analysis/bin/python $TOOLS_PATH/LiveOcean_BCs.py $DATE
