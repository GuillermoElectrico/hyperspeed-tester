#!/bin/bash
echo *******Updating respositories*******
sleep 2
apt-get update
echo *******Installing IPerf3*******
sleep 2
apt-get install iperf3 -y
echo *******Setting Cron to execute on startup for script execution********
(crontab -l 2>/dev/null; echo "* * * * * iperf3 -s -D") | crontab -
echo *******Setup complete*******
sleep 2
