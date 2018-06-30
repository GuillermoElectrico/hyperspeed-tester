import netifaces
import wiringpi2
import subprocess
import time
import os
from uuid import getnode as get_mac

script_folder = "/home/iperf-scripts"

##This script is used to make the two buttons on the LCD screen operational

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

wiringpi2.wiringPiSetup()
# --LCD
lcdHandle = wiringpi2.lcdInit(LCD_ROW, LCD_COL, LCD_BUS,
PORT_LCD_RS, PORT_LCD_E,
PORT_LCD_D4, PORT_LCD_D5,
PORT_LCD_D6, PORT_LCD_D7, 0, 0, 0, 0);
lcdRow = 0 # LCD Row
lcdCol = 0 # LCD Column
# --LCD

wiringpi2.pinMode(5,0)
wiringpi2.pinMode(6,0)

###Screen Outputs

def ScreenOutput(TopLine, BottomLine):

    wiringpi2.lcdClear(lcdHandle)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow)
    wiringpi2.lcdPrintf(lcdHandle, TopLine)
    wiringpi2.lcdPosition(lcdHandle, lcdCol, lcdRow + 1)
    wiringpi2.lcdPrintf(lcdHandle, BottomLine)

while (1 == 1):
    if wiringpi2.digitalRead(5) == 0:
        ScreenOutput("Stopping Scripts", "Please Wait...")
        ##Launch shell script to terminate any running testing scripts
        subprocess.call([script_folder + "/button_shell_script_doble_host.sh"])
        time.sleep(3)
        ScreenOutput("Select Server", "<-Core1||Core2->")
        time.sleep(3)
        while (wiringpi2.digitalRead(6) == 1 and wiringpi2.digitalRead(5) == 1):
            time.sleep(1)
        if wiringpi2.digitalRead(5) == 0:
            ScreenOutput("Restart Script1", "Please Wait...")
            time.sleep(3)
            os.system("python " + script_folder + "/execute_test_final_doble_host1.py > /dev/null 2>&1 &")
        elif wiringpi2.digitalRead(6) == 0:
            ScreenOutput("Restart Script2", "Please Wait...")
            time.sleep(3)
            os.system("python " + script_folder + "/execute_test_final_doble_host2.py > /dev/null 2>&1 &")
    elif wiringpi2.digitalRead(6) == 0:
        time.sleep(3)
        if wiringpi2.digitalRead(6) == 0:
            subprocess.call([script_folder + "/button_shell_script_doble_host.sh"])
            ScreenOutput("Shutdown?", "<- Yes  |  No ->")
            time.sleep(3)
            while (wiringpi2.digitalRead(6) == 1 and wiringpi2.digitalRead(5) == 1):
                time.sleep(1)
            if wiringpi2.digitalRead(5) == 0:
                ScreenOutput("Shutting Down", "")
                time.sleep(1)
                os.system("sudo shutdown now")
                time.sleep(1)
                while (1 == 1):
                    time.sleep(1)
            ScreenOutput("No Shutdown", "")
            time.sleep(3)
        elif wiringpi2.digitalRead(5) == 0:
            subprocess.call([script_folder + "/button_shell_script_doble_host.sh"])
            ScreenOutput("Delete logs?", "<- Yes  |  No ->")
            time.sleep(3)
            while (wiringpi2.digitalRead(6) == 1 and wiringpi2.digitalRead(5) == 1):
                time.sleep(1)
            if wiringpi2.digitalRead(5) == 0:
                ScreenOutput("All logs deleted", "")
                time.sleep(1)
                os.system("sudo rm /home/iperf/*")
                time.sleep(2)
            else:
                ScreenOutput("Nothing deleted", "")
                time.sleep(3)
        else:
            subprocess.call([script_folder + "/button_shell_script_doble_host.sh"])
            try:
                board_mac = get_mac() 
                IPAddr = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr'] 
                formatted_board_mac = str(''.join(("%012X" % board_mac)[i:i+2] for i in range(0, 12, 2)))
                #firstpart, secondpart = formatted_board_mac[:len(formatted_board_mac)/2], formatted_board_mac[len(formatted_board_mac)/2:]
                ScreenOutput(formatted_board_mac, str(IPAddr))
            except:
                ScreenOutput("Not Ethernet", "Connect cable")
            time.sleep(5)
            while (wiringpi2.digitalRead(6) == 1 and wiringpi2.digitalRead(5) == 1):
                time.sleep(1)
        ScreenOutput("Select Server", "<-Core1||Core2->")
        time.sleep(3)
        while (wiringpi2.digitalRead(6) == 1 and wiringpi2.digitalRead(5) == 1):
            time.sleep(1)
        if wiringpi2.digitalRead(5) == 0:
			ScreenOutput("Restart Script1", "Please Wait...")
			time.sleep(3)
			os.system("python " + script_folder + "/execute_test_final_doble_host1.py > /dev/null 2>&1 &")
        elif wiringpi2.digitalRead(6) == 0:
			ScreenOutput("Restart Script2", "Please Wait...")
			time.sleep(3)
			os.system("python " + script_folder + "/execute_test_final_doble_host2.py > /dev/null 2>&1 &")
