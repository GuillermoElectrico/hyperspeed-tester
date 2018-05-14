echo *******Updating Repositories*******
sleep 2
apt-get update
echo *******Installing dependencies MySQL-python*******
sleep 2
apt install libmysqlclient-dev libmariadbclient-dev
echo *******Installing PIP for Flask Installation*******
sleep 2
apt-get install python-pip -y
pip install --upgrade pip
echo *******Installing database gestions*******
sleep 2
pip install MySQL-python
echo *******Installing RSSH for RCP Pulls*******
sleep 2
apt-get install rssh -y
echo ******Creating directories required for logs*******
sleep 2
mkdir /home/iperf-scripts
mkdir /home/iperf
mkdir /home/test-logs
echo ******Copying scripts*******
sleep 2
wget -O /home/iperf-scripts/json_server_side.py https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Server-Script/json_server_side.py
echo *******Setting Cron to execute on startup for script execution********
(crontab -l 2>/dev/null; echo "* * * * * python /home/iperf-scripts/json_server_side.py") | crontab -
echo *******Setup complete*******
sleep 2