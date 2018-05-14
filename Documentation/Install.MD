# Installation Steps
The following contains the necessary actions to take to ensure the system functions as a whole.

## Odroid Ubuntu MATE Install

Go to:
http://adjarvis.com/odroid-c2-ubuntu-install/

## Odroid Board Installation Simple (Only test to iperf server, only local log. Perfect to test networks without Internet access or remote log access. Example: use public iperf servers)
The necessary files and packages are included in the install script. The script is a very basic method to list the required packages and install them. It is in no way indestructible. In the event of issues the packages can be manually installed. On top of the packages there are a couple of directories we use by default:

* /home/iperf
* /home/iperf-scripts

These can be changed freely but will be created in the install script.

To install with the script go to the 'odroid-simple-install_script.sh' in Installation-Scripts

	1. Copy the script to odroid board - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/odroid-simple-install_script.sh

	2. Chmod file so that you can run it 'chmod u+x odroid-simple-install_script.sh'

	3. Run the odroid-simple-install_script.sh file
	
In addition to the necessary packages the following scripts need to be included on the Odroid board:

* boot.py
* button_script_simple.py
* button_shell_script_simple.sh
* execute_test_final_simple.py

By default all of these are stored in the /home/iperf-scripts folder. All of the necessary packages for the Odroid board can be found in Client-Script. They are all installed as part of the install script and do not need to be manually put on there.

## Odroid Board Installation ookla (Only test to speedtest by ookla servers. Perfect to test networks with only Internet access without remote log access or iperf server. Example: use public networks)
The necessary files and packages are included in the install script. The script is a very basic method to list the required packages and install them. It is in no way indestructible. In the event of issues the packages can be manually installed. On top of the packages there are a couple of directories we use by default:

* /home/iperf-scripts

These can be changed freely but will be created in the install script.

To install with the script go to the 'odroid-ookla-install_script.sh' in Installation-Scripts

	1. Copy the script to odroid board - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/odroid-ookla-install_script.sh

	2. Chmod file so that you can run it 'chmod u+x odroid-ookla-install_script.sh'

	3. Run the odroid-ookla-install_script.sh file
	
In addition to the necessary packages the following scripts need to be included on the Odroid board:

* boot.py
* button_script_ookla.py
* button_shell_script_ookla.sh
* execute_test_final_ookla.py

By default all of these are stored in the /home/iperf-scripts folder. All of the necessary packages for the Odroid board can be found in Client-Script. They are all installed as part of the install script and do not need to be manually put on there.

## Odroid Board Installation
The necessary files and packages are included in the install script. The script is a very basic method to list the required packages and install them. It is in no way indestructible. In the event of issues the packages can be manually installed. On top of the packages there are a couple of directories we use by default:

* /home/iperf
* /home/iperf-scripts

These can be changed freely but will be created in the install script.

To install with the script go to the 'odroid-install_script.sh' in Installation-Scripts

	1. Copy the script to odroid board - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/odroid-install_script.sh

	2. Chmod file so that you can run it 'chmod u+x odroid-install_script.sh'

	3. Run the odroid-install_script.sh file
	
In addition to the necessary packages the following scripts need to be included on the Odroid board:

* boot.py
* button_script.py
* button_shell_script.sh
* execute_test_final.py

By default all of these are stored in the /home/iperf-scripts folder. All of the necessary packages for the Odroid board can be found in Client-Script. They are all installed as part of the install script and do not need to be manually put on there.

## Odroid Board Installation dual server (especial version for Euskal Enconter, 2 server iperf3 selectable via button)
The necessary files and packages are included in the install script. The script is a very basic method to list the required packages and install them. It is in no way indestructible. In the event of issues the packages can be manually installed. On top of the packages there are a couple of directories we use by default:

* /home/iperf-scripts

These can be changed freely but will be created in the install script.

To install with the script go to the 'odroid-ookla-install_script.sh' in Installation-Scripts

	1. Copy the script to odroid board - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/odroid-dual-install_script.sh

	2. Chmod file so that you can run it 'chmod u+x odroid-dual-install_script.sh'

	3. Run the odroid-dual-install_script.sh file
	
In addition to the necessary packages the following scripts need to be included on the Odroid board:

* boot.py
* button_script_doble_host.py
* button_shell_script_doble_host.sh
* execute_test_final_doble_host1.py
* execute_test_final_doble_host2.py

By default all of these are stored in the /home/iperf-scripts folder. All of the necessary packages for the Odroid board can be found in Client-Script. They are all installed as part of the install script and do not need to be manually put on there.

## IPerf Server Installation 
The IPerf server has a relatively small footprint in terms of required packages. The only packages needed are the IPerf.

To install with the script go to the 'iperf-server-install-script.sh' in Installation-Scripts

	1. Copy the script to server - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/iperf-server-install-script.sh

	2. Chmod file so that you can run it 'chmod u+x iperf-server-install-script.sh'

	3. Run the iperf-server-install-script.sh file 
	
Of importance as well is the cron jobs that are run on the server. The required ones can be found in Server-Script.
	
## IPerf Log Server Installation
The IPerf log server is where things are a bit more tricky. This server store the logs for the tests along with the front-end interface to display them. For the server we have used a simple LAMP deployment (Apache, MySQL, PHP), however this can be changed. As such the installation guide for LAMP stack installation on Ubuntu should be followed here:

* https://clouding.io/kb/como-instalar-en-linux-apache-mariadb-y-php-lamp/

We also made use of a basic database structure consisting of just two tables to store all the data we need. We have the following two tables:

* Engineer to board mappings
* IPerf test results

The following SQL snippets are below for both tables:

```SQL
CREATE TABLE `engineer_assignment`(
  `engineer_id` INT(11) DEFAULT NULL,
  `engineer_name` VARCHAR(255) NOT NULL,
  `engineer_email` VARCHAR(255) NOT NULL,
  `board_id` VARCHAR(255) NOT NULL
);
```
```SQL
CREATE TABLE `test_logs_upload`(
  `log_id` INT(11) DEFAULT NULL,
  `file_hash` VARCHAR(255) NOT NULL,
  `timestamp` INT(255) NOT NULL,
  `connecting_to` VARCHAR(255) NOT NULL,
  `test_duration` VARCHAR(255) NOT NULL,
  `mbps_sent` VARCHAR(255) NOT NULL,
  `mbps_received` VARCHAR(255) NOT NULL,
  `board_id` VARCHAR(255) NOT NULL,
  `gateway_mac` VARCHAR(255) DEFAULT NULL,
  `gateway_ip` VARCHAR(255) NOT NULL,
  `peak_mbps` VARCHAR(255) NOT NULL,
  `ookla_send` VARCHAR(255) NOT NULL,
);
```

```SQL
CREATE TABLE `test_logs_download`(
  `log_id` INT(11) DEFAULT NULL,
  `file_hash` VARCHAR(255) NOT NULL,
  `timestamp` INT(255) NOT NULL,
  `connecting_to` VARCHAR(255) NOT NULL,
  `test_duration` VARCHAR(255) NOT NULL,
  `mbps_sent` VARCHAR(255) NOT NULL,
  `mbps_received` VARCHAR(255) NOT NULL,
  `board_id` VARCHAR(255) NOT NULL,
  `gateway_mac` VARCHAR(255) DEFAULT NULL,
  `gateway_ip` VARCHAR(255) NOT NULL,
  `peak_mbps` VARCHAR(255) NOT NULL,
  `ookla_received` VARCHAR(255) NOT NULL
);
```

On top of this the only other package needed is RSSH for the RCP copies between log server and iperf server. Of importance as well is the cron jobs that are run on the server. The required cron jobs can be found in Server-Script.

The following scripts are needed on the IPerf log server:

* json_server_side.py

To install: 

	1. Copy the script to server - wget https://raw.githubusercontent.com/GuillermoElectrico/hyperspeed-tester/master/Installation-Scripts/iperf-log-server-install-script.sh

	2. Chmod file so that you can run it 'chmod u+x iperf-log-server-install-script.sh'

	3. Run the iperf-log-server-install-script.sh file 


By default these are in the /home/iperf-scripts installation directory.

For the front-end we used Semantic for the stlying of the webpage. If using the same webpage this will need to be installed as well. This can be done through the information from Semantic here:

* https://semantic-ui.com/introduction/getting-started.html

## Additional Configurations
There are a couple of items that require manual configurations depending on the environment. The following needs to be done:

* Copying between the Odroid and the IPerf server is done using SCP. In order to do this we use a specific user on the IPerf server dedicated to the copying from the Odroid boards. The user for this needs to be created on the IPerf server. We use public and private keys for authentication however this can be changed.
* Copying between the IPerf Server and Iperf Log Server is very similar. We use RCP to copy the files from the IPerf server using a dedicated account for this purpose. Therefore the account needs to be created on the IPerf server for this. Again we use public and private keys for authentication with this account but this can be changed.

## Script Changes
The scripts on this repository use placeholders for various values that need to be assigned in accordance with the environment in which it is run. The following need to be updated in execute_test_final.py or execute_test_final_simple.py:

* Hostname - The hostname of the IPerf server that the tests will be run against.
* Hostport - The port of the IPerf server that the tests will be run against.
* scphost - The hostname of the log server that upload tests results.
* scpport - The port of the log server that upload tests results.
* scpuser - The user is used to copy the files to the log server.
* scppass - The password is used to copy the files to the log server.
* hostweb - The hostname of the web server to obtain the external CPE IP in json format (use whats-mi-ip.php include in Web-Front-End folder).

If you want to test against a specific server modify in execute_test_final.py (to compare results if there is internet)
* servers = []

The following needs to be changed in json_server_side.py:

* DB Information - For the DB connection the necessary information for the database being used need to be substituted such as database name, password, username etc.

