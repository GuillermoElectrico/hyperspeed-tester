## Below are the required CRON jobs that need to be run on the Odroid board.

* @reboot python /home/iperf-script/button_script_doble_host.py
* @reboot sleep 1; python /home/iperf-script/boot.py
* @reboot sleep 32; python /home/iperf-script/execute_test_final_doble_host1.py

These run the relevant scripts needed for the board. The first being the boot and button script for button operation on the board on boot up. 30 seconds after booting it executes the speed test script.
