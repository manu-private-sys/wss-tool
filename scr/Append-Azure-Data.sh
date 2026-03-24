#!/bin/bash
# Initialize cache script to append Azure Sites data to WSS-TOOL cache files at /tmp/WSS-TOOL/SITE-REGIONS
# This needs to be scheduled as a cron in order to get it executed daily

dir_path="/tmp/WSS-TOOL/SITE-REGIONS/";

conc_filename="concentrator.csv"
proxy_filename="proxysg.csv";

printf "\nAppending Azure data at : `date`";

printf "\nAppending Azure Concentrator data ...";
cd $dir_path;
cat azure-concentrator.csv >> $conc_filename;

printf "\nAppending Azure ProxySG data ...";
cd $dir_path;
cat azure-proxysg.csv >> $proxy_filename;

printf "\nAzure data appended succesfully!\n\n"
