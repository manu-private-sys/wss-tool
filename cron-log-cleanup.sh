#!/bin/bash
# Cleanup Script to clear unwanted files from /tmp/WSS-TOOL and empty log files
# This needs to be scheduled as a cron in order to get it executed weekly

> /tmp/WSS-TOOL/LOGS/cleanup-cron.log;
echo "Emptied cleanup-cron.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Initialize-GCP-Cache.log;
echo "Emptied Initialize-GCP-Cache.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Fetch-Concentrator-Status.log;
echo "Emptied Fetch-Concentrator-Status.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/DNS-Check-ProxySG.log;
echo "Emptied DNS-Check-ProxySG.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Active-Session-Download.log;
echo "Emptied Active-Session-Download.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Force-Core-Dump.log;
echo "Emptied Force-Core-Dump.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Automated-Concentrator-Login.log;
echo "Emptied Automated-Concentrator-Login.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/Automated-ProxySG-Login.log;
echo "Emptied Automated-ProxySG-Login.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/ProxySG-Certificate-Revocation.log;
echo "Emptied ProxySG-Certificate-Revocation.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/ProxySG-Restart-Regular.log;
echo "Emptied ProxySG-Restart-Regular.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log

> /tmp/WSS-TOOL/LOGS/ProxySG-Status.log;
echo "Emptied ProxySG-Status.log on `date`" >> /tmp/WSS-TOOL/LOGS/cleanup-cron.log
