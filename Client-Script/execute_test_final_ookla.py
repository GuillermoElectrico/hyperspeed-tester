##Modules required for operation
import os
import socket
import sys
import shutil
import wiringpi2
import time
import requests
import speedtest
import signal
import time

## Seedtest Ookla
servers = []
# If you want to test against a specific server
# servers = [1234]

#Define global variables
ookla_upload = ""
ookla_download = ""
ookla_test = False
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

##Function will perform another speed test as well for comparison using Ookla's speedtest.net
def perform_ookla_test():
    global ookla_upload
    global ookla_download
    ScreenOutput("Performing Ookla", "Speedtest...")
    ookla = speedtest.Speedtest()
    ookla.get_servers(servers)
    ookla.get_best_server()
	#Led3
    wiringpi2.digitalWrite(LED3,1)
    ScreenOutput('Speed Test Ookla', 'Upload...')
    time.sleep(1)
    ookla_upload = ookla.upload() / 1000000
    ookla_upload = round(ookla_upload, 2)
    print ookla_upload
	#Led4
    wiringpi2.digitalWrite(LED4,1)
    ScreenOutput('Speed Test Ookla', 'Download...')
    time.sleep(1)
    ookla_download = ookla.download() / 1000000
    ookla_download = round(ookla_download, 2)
    print ookla_download
	#Led5
    wiringpi2.digitalWrite(LED5,1)
    ScreenOutput('Speed Test Ookla', 'Finished')
    time.sleep(1)

  

##Function will run the Line Test
def runTest() :
    global ookla_upload
    global ookla_download
    global ookla_test

    ##Perform an Ookla Speedtest with a 60 second timeout
	#Led2
    wiringpi2.digitalWrite(LED2,1)
    ookla_results = {}
    ookla_test = True
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60)
    try:
        ookla_results = perform_ookla_test()
    except Exception as ex:
        ookla_test = False
        if "timed_out" in ex:
            ookla_upload = "---"
            ookla_download = "---"
        else:
            ookla_upload = "---"
            ookla_download = "---"
    finally:
        signal.alarm(0)

    
 
##Function actually conducts the test and performs the checks
def executeTesting():
    global ookla_upload
    global ookla_download
    global ookla_test
	
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
    ##Execute the test
	#Led1
    wiringpi2.digitalWrite(LED1,1)
    runTest()

    if ookla_test == True :
		#Led6
        wiringpi2.digitalWrite(LED6,1)
		#Led7
        wiringpi2.digitalWrite(LED7,1)
        ##Execute an infinite while loop to loop the screen output at the end of the test
        while True:
			##Display the upload speed 
			ScreenOutput('Upload ookla:', str(round(ookla_upload, 2)) + " Mbps" )
			time.sleep(3)
			##Display the download speed 
			ScreenOutput('Download ookla:', str(round(ookla_download, 2)) + " Mbps")
			time.sleep(3)
    else:
        ##If the ping test fails meaning no connectivity to the IPerf server then restart the test again
        ScreenOutput('Test Failed', 'Retrying...')
        time.sleep(3)
        executeTesting()
##Execute the Line Test for the first time
executeTesting()
