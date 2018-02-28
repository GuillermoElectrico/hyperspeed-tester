import json
import glob
import MySQLdb
import os
import shutil
import pwd
import grp
import calendar
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# This is the server side script that runs repeatedly to collect the results
# that are FTP'd from the client/LineTester. It then extracts the JSON data and
# inserts it into the mySQL database, stores the log file in another directory
# and removes the old file.

log_files = "/home/iperf"
final_log_store = "/home/test-logs"

#The single function that runs all
def run_script():
    #Get list of the files in the directory
    dir_list = glob.glob(log_files + "/*")

    #For every file in the dir
    for file_name in dir_list:
        with open(file_name) as json_data:
            #Load JSON form each file in this for loop
            jdata = json.load(json_data)

        #Extract all needed JSON elements
        counter = 0
        speed_interval_list = list()
        for x in jdata["intervals"]:
            var = jdata['intervals'][counter]['sum']['bits_per_second']
            speed_interval_list.append(var)
            counter = counter+1

        test_duration =  jdata['start']['test_start']['duration']
        connecting_to =  jdata['start']['connecting_to']['host']
        sent_bps = jdata['end']['sum_sent']['bits_per_second']
        received_bps =  jdata['end']['sum_received']['bits_per_second']
        mac_address =  jdata['end']['host_information']['mac_address']
        hash_value = jdata['end']['host_information']['hash']
        gateway_mac = jdata['end']['host_information']['gateway_mac']
        gateway_ip = jdata['end']['host_information']['gateway_ip']
        peak = max(speed_interval_list)
        direction = jdata['end']['test_information']['direction']
        #Set the time stamp to the server time
        timestamp_ = calendar.timegm(time.gmtime())
    	mac_address_q = "'" + mac_address + "'"
    	print mac_address_q
        #Convert from bps to mega bps
        sent_mbps = sent_bps / 1000000
        received_mbps = received_bps / 1000000
        peak_mbps = peak / 1000000

        #In this loop we are inserting all the data into the database
        #In this loop we are inserting all the data into the database

        #Server Connection to MySQL params
        conn = MySQLdb.connect(host= "X.X.X.X",
                          user="db-user",
                          passwd="db-pass",
                          db="db-name")
        x = conn.cursor()
		
		#Try Except statment to catch if the insert was sucsessful or not
        #If it was not then it rolls back
        print direction
        if direction == "up" :
			try:
				x.execute("INSERT INTO test_logs_upload VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (hash_value, timestamp_, connecting_to, test_duration, sent_mbps, received_mbps, mac_address, gateway_mac, gateway_ip, peak_mbps))

				conn.commit()
			except:
				print(x._last_executed)
				conn.rollback()
				#Close DB connection
				conn.close()
			#Here is where we move the file into a perminant log directory
			#Define path value including the file hash from the JSON
			path_to_file = final_log_store + "/" + hash_value + "_Upload"
			#Move the file to the new directory
			shutil.move(log_files + "/" + hash_value + "_Upload", path_to_file)
			#Change the ownership of the file so that www-data is the owner. This
			#allows for the JSON file downloads from the apache webserver to work
			os.chown(path_to_file, pwd.getpwnam("www-data").pw_uid, grp.getgrnam("www-data").gr_gid)
        elif direction == "down" :
			try:
				x.execute("INSERT INTO test_logs_download VALUES (Null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (hash_value, timestamp_, connecting_to, test_duration, sent_mbps, received_mbps, mac_address, gateway_mac, gateway_ip, peak_mbps))

				conn.commit()
			except:
				print(x._last_executed)
				conn.rollback()
				#Close DB connection
				conn.close()
			#Here is where we move the file into a perminant log directory
			#Define path value including the file hash from the JSON
			path_to_file = final_log_store + "/" + hash_value + "_Download"
			#Move the file to the new directory
			shutil.move(log_files + "/" + hash_value + "_Download", path_to_file)
			#Change the ownership of the file so that www-data is the owner. This
			#allows for the JSON file downloads from the apache webserver to work
			os.chown(path_to_file, pwd.getpwnam("www-data").pw_uid, grp.getgrnam("www-data").gr_gid)


#On boot we run this python script as a cron job which can only be done every
#mintue so uing this look it allows the script to run every 15 seconds to
#speed up the time it takes to display the results on the front end.
#This is pretty crappy but it works :)
for t in range(60,-1,-1):
    seconds = t % 60
    time.sleep(1.0)
    if seconds == 59:
        run_script()
    elif seconds == 45:
        run_script()
    elif seconds == 30:
        run_script()
    elif seconds == 15:
        run_script()
