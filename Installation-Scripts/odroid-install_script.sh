#!/bin/bash
echo *******Updating respositories*******
sleep 2
apt-get update
echo *******Installing IPerf3*******
sleep 2
apt-get install iperf3 -y
echo *******Installing PIP*******
sleep 2
apt-get install python-pip -y
pip install --upgrade pip
echo *******Installing required files for paramiko*******
sleep 2
apt-get install build-essential libssl-dev libffi-dev python3-dev
echo *******Installing paramiko*******
sleep 2
pip install paramiko
echo *******Installing required files for SCP*******
sleep 2
apt-get install libffi6 libffi-dev -y
echo *******Installing SCP*******
sleep 2
pip install scp
echo *******Installing SCPClient*******
sleep 2
pip install SCPClient
echo *******Installing SSHClient*******
sleep 2
pip install SSHClient
echo *******Installing ARP module for Python*******
sleep 2
pip install python_arptable
echo *******Installing network interface module for Python*******
sleep 2
pip install netifaces
echo *******Creating directory for iperf files*******
sleep 2
mkdir /home/iperf
mkdir /home/iperf-scripts
sleep 2
echo *******Installing Git for Odroid Screen Package******
apt-get install git -y
sleep 2
echo ******Installing dependencies for Odroid Screen******
apt-get install python-dev python-setuptools swig3.0 -y
echo ******Copying Screen Package from Git********
mkdir /home/screen
git clone https://github.com/hardkernel/WiringPi2-Python.git
cd WiringPi2-Python
git submodule init
git submodule update
sleep 2
echo *******Building Screen Package*******
swig3.0 -python -threads wiringpi.i
python setup.py build install
rm /etc/modprobe.d/blacklist-w1.conf
echo "blacklist w1_gpio">> /etc/modprobe.d/blacklist-w1.conf
sleep 2
echo *******Installing Ookla Speedtest for Python********
pip install speedtest-cli
sleep 2
echo *******Installing Python Requests module********
pip install requests
sleep 2
echo *******Importing subprocess module for Python********
cd /home
git clone https://github.com/google/python-subprocess32
cd python-subprocess32
python setup.py install
sleep 2
echo *******Installing OpenSSH Server********
apt-get install openssh-server -y
sleep 2
echo ******Copying scripts*******
wget -O /home/iperf-scripts/execute_test_final.py https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Client-Script/execute_test_final.py
wget -O /home/iperf-scripts/boot.py https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Client-Script/boot.py
wget -O /home/iperf-scripts/button_script.py https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Client-Script/button_script.py
wget -O /home/iperf-scripts/button_shell_script.sh https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Client-Script/button_shell_script.sh
chmod +x /home/iperf-scripts/button_shell_script.sh
sleep 2
echo *******Setting Cron to execute on startup for script execution********
(crontab -l 2>/dev/null; echo "@reboot python /home/iperf-scripts/button_script.py") | crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 1; python /home/iperf-scripts/boot.py") | crontab -
(crontab -l 2>/dev/null; echo "@reboot sleep 32; python /home/iperf-scripts/execute_test_final.py") | crontab -
echo *******Setup complete*******
sleep 2
