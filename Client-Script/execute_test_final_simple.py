##Modules required for operation
import os
import socket
import sys
import hashlib
import json
import shutil
import wiringpi2
import time
import python_arptable
import requests
import subprocess32 as subprocess
import netifaces
import signal
import time
from python_arptable import get_arp_table
from uuid import getnode as get_mac

##Set the hostname an hostport of the iperf server to perform tests againsts
hostname = "X.X.X.X"
hostport = "5201"
log_files = "/home/iperf"

#Define global variables
sent_mbps = ""
received_mbps = ""
peak = ""
############### Deals with screen initialisation on the board ###############
# --LCD
LCD_ROW = 2 # 16 Char
LCD_COL = 16 # 2 Line
LCD_BUS = 4 # Interface 4 Bit mode

PORT_LCD_RS = 7 # GPIOY.BIT3(#83)
PORT_LCD_E = 0 # GPIOY.BIT8(#88)
PORT_LCD_D4 = 2 # GPIOX.BIT19(#116)
PORT_LCD_D5 = 3 # GPIOX.BIT18(#115)
PORT_LCD_D6 = 1 # GPIOY.BIT7(#87)
PORT_LCD_D7 = 4 # GPIOX.BIT4(#104)
# --Buttons
PORT_LCD_5 = 5

# --LCD
##Initialise the screen
wiringpi2.wiringPiSetup()
# --LCD
lcdHandle = wiringpi2.lcdInit(LCD_ROW, LCD_COL, LCD_BUS,
PORT_LCD_RS, PORT_LCD_E,
PORT_LCD_D4, PORT_LCD_D5,
PORT_LCD_D6, PORT_LCD_D7, 0, 0, 0, 0);
lcdRow = 0 # LCD Row
lcdCol = 0 # LCD Column
# --LCD

# --LED
LED1 = 21 
wiringpi2.pinMode(LED1,1)
wiringpi2.digitalWrite(LED1,0)
LED2 = 22
wiringpi2.pinMode(LED2,1)
wiringpi2.digitalWrite(LED2,0)
LED3 = 23
wiringpi2.pinMode(LED3,1)
wiringpi2.digitalWrite(LED3,0)
LED4 = 24
wiringpi2.pinMode(LED4,1)
wiringpi2.digitalWrite(LED4,0)
LED5 = 11
wiringpi2.pinMode(LED5,1)
wiringpi2.digitalWrite(LED5,0)
LED6 = 26
wiringpi2.pinMode(LED6,1)
wiringpi2.digitalWrite(LED6,0)
LED7 = 27
wiringpi2.pinMode(LED7,1)
wiringpi2.digitalWrite(LED7,0)
# --LED

##Function displays the TopLine and BottomLine message passed on the screen
def ScreenOutput(TopLine, BottomLine):
    wiringpi2.lcdClear(lcdHandle)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow)
    wiringpi2.lcdPrintf(lcdHandle, TopLine)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow + 1)
    wiringpi2.lcdPrintf(lcdHandle, BottomLine)

##Create a function that will raise a timeout error when called
def timeout_handler(num, stack):
    raise Exception("timed_out")
    
##Function performs a ping test against the server to ensure that it is accessible
def pingHome():
    ScreenOutput('Ping Test', 'Executing...')
    time.sleep(1)
    ##Perform an OS command to execute the ping test
    response = os.system("ping -c 2 " + hostname)
    status = ""
    print(response)

    ##Check the result to see whether the pings were successful
    if response == 0:
      print hostname, 'is up!'
      status = True
      ScreenOutput('Ping Test', 'Succesful')
      time.sleep(1)
    else:
      print hostname, 'is down!'
      status = False
      ScreenOutput('Ping Test', 'Unsuccessful')
      time.sleep(3)
    return status

##Function performs a check against the default IPerf port 5201 to ensure it is up
def testIperfSocket() :
    #check iperf is running on the host by establishing the socket the port 5201
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((hostname, int(hostport)))
    if result == 0:
        sock.shutdown(socket.SHUT_RDWR)
        ##Close the socket otherwise the server thinks a test is still occurring which prevents any further tests
        sock.close()
        ScreenOutput('Iperf Connection', 'Succesful')
        time.sleep(1)
        return True
    else:
        ScreenOutput('Iperf Connection', 'Unsuccessful')
        time.sleep(3)
        ScreenOutput('Test Failed', 'Retrying...')
        time.sleep(1)
        ##Rerun the test if the IPerf connection fails
        executeTesting()
        return False
		
##Function will obtain the default gateway Ip address
def get_dg_ip():
    ##Grab the default gateway address
    gws = netifaces.gateways()
    gateway_address_list = gws['default'][netifaces.AF_INET]
    gateway_address = gateway_address_list[0]

    return gateway_address
		
##Function will obtain the default gateway MAC address
def get_dg_mac(gateway_ip): 

    ##Import the contents of the ARP table for reading
    arp_table = get_arp_table()
    ##Loop through each ARP entry to check whether the gateway address is present
    for arp_entry in arp_table:
        if arp_entry["IP address"] == gateway_ip:
            ##Grab the MAC address associated with the gateway address
            gateway_mac = arp_entry["HW address"]

    return gateway_mac
	
##Function will take the returned JSON and append new required values on the end
def edit_json(hashed_file_name, gateway_mac, gateway_ip) :

	##Obtain the MAC address of the board
    board_mac = get_mac()
    ##Format the MAC address into a common form
    formatted_board_mac = str(':'.join(("%012X" % board_mac)[i:i+2] for i in range(0, 12, 2)))
    print formatted_board_mac
	
    ##Open the file Upload and read the contents
    file_path = log_files + "/" + hashed_file_name + "_Upload"
    f = open(file_path, 'r')
    file_contents = f.read()
    f.close()

    ##Load in the contents of the file and convert to a JSON object
    json_file_contents = json.loads(file_contents)
    ##Add the new JSON values onto the end, the boards MAC address, the file hash, and the gateway MAC
    json_file_contents["end"]["host_information"] = {"mac_address": formatted_board_mac, "hash": hashed_file_name, "gateway_mac": gateway_mac, "gateway_ip": gateway_ip}
    
    ##Dump the new JSON information into the file
    json.dump(json_file_contents, open(file_path, "w"))
	
	##Open the file Download and read the contents
    file_path = log_files + "/" + hashed_file_name + "_Download"
    f = open(file_path, 'r')
    file_contents = f.read()
    f.close()

    ##Load in the contents of the file and convert to a JSON object
    json_file_contents = json.loads(file_contents)
    ##Add the new JSON values onto the end, the boards MAC address, the file hash, and the gateway MAC
    json_file_contents["end"]["host_information"] = {"mac_address": formatted_board_mac, "hash": hashed_file_name, "gateway_mac": gateway_mac, "gateway_ip": gateway_ip}
    
    ##Dump the new JSON information into the file
    json.dump(json_file_contents, open(file_path, "w"))
    
##Function will run the Line Test
def runTest() :
    global sent_mbps
    global received_mbps
    global hostname
    global hostport
    global peak

    ScreenOutput('Speed Test', 'Executing...')
    time.sleep(1)
	
    ScreenOutput('Speed Test', 'Upload...')
    time.sleep(1)

    ##Try and execute the IPerf test Upload. Specifies a timeout of 14 seconds for the IPerf connection
    try:
        procId = subprocess.run(["iperf3", "-c", hostname, "-p", hostport, "-J", "-t", "15", "-Z" ], stdout=subprocess.PIPE, timeout=30)
        print hostname
    ##Raise an error if the timeout expires and re-run the test
    except subprocess.TimeoutExpired:
        ScreenOutput('Speed Test', 'Failed')
        time.sleep(3)
        executeTesting()
    ##Take the stdout and convert to JSON from the executed command
    json_output = procId.stdout

    ##Write the JSON to the file
    f = open(log_files + '/resultsUpload.json', 'w+')
    string_to_write = str(json_output)
    f.write(string_to_write)
    f.close()

    file_name = log_files + "/resultsUpload.json"

    ##Open the JSON file just created
    with open(file_name) as json_data:
        jdata = json.load(json_data)

    ##Check to see whether the JSON entered into the file is from a successful test and not a server
    ##busy message
    try:
        ##Extract the sent BPS for screen output
        sent_bps = jdata['end']['sum_sent']['bits_per_second']

    ##Display the error if the server is busy if the JSON is not complete
    except:
        ScreenOutput('Server Busy', 'Retrying')
        time.sleep(3)
        ##Rerun the test again
        executeTesting()

    ##Convert the bps into gbps
    sent_mbps = sent_bps / 1000000
    print str(sent_mbps)
	
    ScreenOutput('Speed Test', 'Download...')
    time.sleep(1)

    ##Try and execute the IPerf test Download. Specifies a timeout of 14 seconds for the IPerf connection
    try:
        procId = subprocess.run(["iperf3", "-c", hostname, "-p", hostport, "-J", "-t", "15", "-Z", "-R" ], stdout=subprocess.PIPE, timeout=30)
        print hostname
    ##Raise an error if the timeout expires and re-run the test
    except subprocess.TimeoutExpired:
        ScreenOutput('Speed Test', 'Failed')
        time.sleep(3)
        executeTesting()
    ##Take the stdout and convert to JSON from the executed command
    json_output = procId.stdout

    ##Write the JSON to the file
    f = open(log_files + '/resultsDownload.json', 'w+')
    string_to_write = str(json_output)
    f.write(string_to_write)
    f.close()

    file_name = log_files + "/resultsDownload.json"

    ##Open the JSON file just created
    with open(file_name) as json_data:
        jdata = json.load(json_data)

    ##Check to see whether the JSON entered into the file is from a successful test and not a server
    ##busy message
    try:
        ##Extract the received BPS for screen output
        received_bps =  jdata['end']['sum_received']['bits_per_second']
        counter = 0
        speed_interval_list = list()
        for x in jdata["intervals"]:
            var = jdata['intervals'][counter]['sum']['bits_per_second']
            speed_interval_list.append(var)
            counter = counter+1
        peak = max(speed_interval_list)
        peak = peak / 1000000

    ##Display the error if the server is busy if the JSON is not complete
    except:
        ScreenOutput('Server Busy', 'Retrying')
        time.sleep(3)
        ##Rerun the test again
        executeTesting()

    ##Convert the bps into gbps
    received_mbps = received_bps / 1000000
    print str(received_mbps)
	
    ScreenOutput('Speed Test', 'Finished')
    time.sleep(1)

    ##Read in the contents of the file in order to generate a hash of the data
    with open(file_name) as file_to_hash:
        data = file_to_hash.read()
        md5_hash = hashlib.md5(data).hexdigest()

    ##Take the last 10 characters from the hash to make it shorter
    hash_name = md5_hash[:10]
    new_hash_name = log_files + "/" + hash_name.upper()
    print new_hash_name
    ##Rename the file from resultsUpload.json to the generated hash to uniquely identify the hash
    shutil.move(log_files + "/resultsDownload.json", new_hash_name + "_Download")
    shutil.move(log_files + "/resultsUpload.json", new_hash_name + "_Upload")

    lowerHash = md5_hash[:10]
    ##Convert the hash to uppercase for nicer viewing
    upperHash = lowerHash.upper()

    return upperHash

##Function actually conducts the test and performs the checks
def executeTesting():
    global sent_mbps
    global received_mbps
    global peak
	
    wiringpi2.digitalWrite(LED1,0)
    wiringpi2.digitalWrite(LED2,0)
    wiringpi2.digitalWrite(LED3,0)
    wiringpi2.digitalWrite(LED4,0)
    wiringpi2.digitalWrite(LED5,0)
    wiringpi2.digitalWrite(LED6,0)
    wiringpi2.digitalWrite(LED7,0)

    ##Display that the test is starting
    ScreenOutput('Starting', 'Speed Test')
    time.sleep(2)
    ##Execute the PingHome function in order to check whether there is connectivity to the IPerf Server
    connectionStatus = pingHome()

    if connectionStatus == True :
		#Led1
        wiringpi2.digitalWrite(LED1,1)
        ##Check whether there is connectivity to the IPerf Server on port 5201 for the IPerf test
        testIperfSocket()
		#Led2
        wiringpi2.digitalWrite(LED2,1)
        ##Obtain the hash of the file received from executing the test
        hash_file = runTest()
		#Led3
        wiringpi2.digitalWrite(LED3,1)
        print hash_file
		##Obtain the Ip address of the current gateway
        gateway_ip = get_dg_ip()
		#Led4
        wiringpi2.digitalWrite(LED4,1)
        ##Obtain the MAC address of the current gateway
        gateway_mac = get_dg_mac(gateway_ip)
		#Led5
        wiringpi2.digitalWrite(LED5,1)
        ##Change the JSON file created to include the extra data including gateway MAC, board MAC, and hash
        edit_json(hash_file, gateway_mac, gateway_ip)
		#Led6-7
        wiringpi2.digitalWrite(LED6,1)
        wiringpi2.digitalWrite(LED7,1)
        ##Execute an infinite while loop to loop the screen output at the end of the test
        while True:
            ##Display the test case ID which is equal to the hash
            ScreenOutput('Test ID', hash_file)
            time.sleep(5)
            ##Display the upload speed extracted from the JSON file
            ScreenOutput('Upload:', str(round(sent_mbps, 2)) + " Mbps" )
            time.sleep(2)
            ##Display the download speed extracted from the JSON file
            ScreenOutput('Download:', str(round(received_mbps, 2)) + " Mbps")
            time.sleep(2)
            ##Display the download speed extracted from the JSON file
            ScreenOutput('Peak Download:', str(round(peak, 2)) + " Mbps")
            time.sleep(2)
    else:
        ##If the ping test fails meaning no connectivity to the IPerf server then restart the test again
        ScreenOutput('Test Failed', 'Retrying...')
        time.sleep(3)
        executeTesting()
##Execute the Line Test for the first time
executeTesting()
