#!/bin/bash
# Initialize cache script to generate WSS-TOOL cache files at /tmp/WSS-TOOL/SITE-REGIONS
# This needs to be scheduled as a cron in order to get it executed daily

printf "\nStarting Initialization of the site cache at : `date`";
dir_path="/tmp/WSS-TOOL/SITE-REGIONS/";

conc_filename="concentrator.csv"
proxy_filename="proxysg.csv";

printf "\nSite cache path : %s $dir_path\n";
printf "\nClearing OLD SITE CACHE & Creating new SITE CACHE\n";
cd $dir_path;
printf "\nDetails of Files in $dir_path are : \n";
ls -ahl;
printf "\nClearing old files ...\n";
rm -rf $conc_filename $proxy_filename;
sleep 2;

printf "\nGathering Concentrator info ...";
cd $dir_path;
touch $conc_filename;
chmod 744 $conc_filename;
/snap/bin/gcloud compute instances list --project saas-sed-wss-hp --filter="name~'concentrator' status~'RUNNING'" --format="csv(NAME,ZONE,networkInterfaces[2].networkIP)" > $conc_filename &
pid=$!;
echo "Process with PID $pid is running"
wait $pid;
echo "Process with PID $pid has finished with Exit status: $?"
printf "\nConcentrator info populated at : $dir_path$conc_filename \n";

printf "\nGathering ProxySG info ...";
cd $dir_path;
touch $proxy_filename;
chmod 744 $proxy_filename;
/snap/bin/gcloud compute instances list --project saas-sed-wss-hp --filter="name~'proxysg' status~'RUNNING'" --format="csv(NAME,ZONE,networkInterfaces[2].networkIP)" > $proxy_filename &
pid=$!;
echo "Process with PID $pid is running"
wait $pid;
echo "Process with PID $pid has finished with Exit status: $?"
printf "\nProxySG info populated at : $dir_path$proxy_filename \n";

printf "\nCache files are now populated and upto-date.\n";
printf "\nDetails of Files in $dir_path are : \n";
ls -ahl;
printf "\n\n\n"
