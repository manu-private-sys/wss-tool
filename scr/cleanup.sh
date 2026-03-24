#!/bin/bash
# Cleanup Script to clear unwanted files from /tmp/WSS-TOOL and empty log files
# This needs to be scheduled as a cron in order to get it executed weekly

echo -e "\n" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

echo `date` >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

cd /tmp/WSS-TOOL/ACTIVE-SESSIONS;
rm -rf *;
echo "Cleared all files from ACTIVE-SESSIONS" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

cd /tmp/WSS-TOOL/SSH-CREDS;
rm -rf *;
echo "Cleared all files from SSH-CREDS" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

cd /tmp/WSS-TOOL/CORE-DUMPS;
rm -rf *;
echo "Cleared all files from CORE-DUMPS" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

cd /tmp/WSS-TOOL/TEMP-CORE-DUMP-FILES;
rm -rf *;
echo "Cleared all files from TEMP-CORE-DUMP-FILES" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

echo -e "\n" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log
