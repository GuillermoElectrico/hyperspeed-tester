# Odroid C2 Line Tester 
This is a repository for a portable line tester project. All relevant information can be found in the Documentation folder.

**What we are... Networking university students, What we are not... Coders!** We know that this isn't the best in terms of code quality but if you can/want to improve the code let us know!

## The Aim

To create a portable, cost effective traffic generator that can be used to perform line tests up to a
speed of 1Gbps. The solution should have a front-end that allows for the viewing of test reports and
the necessary systems in place to provide report identification.

Requirements:
  * Be cost effective.
  * Easy to use.
  * Able to test speeds up to 1Gbps.
  * Provide front-end access to test reports.
  * Separate test reports per location.
  
  ## The Solution
  
  In terms of how it all fits together the image below should hopefully show you:
  
  ![alt text](https://github.com/GuillermoElectrico/hyperspeed-tester/blob/master/Documentation/Pictures/Proposal.jpg "Proposal")

1. The user plugs the odroid board into there ISP's provided router
2. A speed test auto-magicaly runs
3. The test ID, Upload and Download speed are displayed on the 16x2 LCD screen
4. The test log is uploaded to the 'Iperf Server' using SCP
5. Using Rsync the test log is pulled from the Iperf Server to the Web/DB Server 
   * This was done as the Iperf server in our case was public facing so it was a little more secure
6. The log is processed by the server side python script and data is inserted into the mySQL table and the log is moved into a permanent storage folder
7. Logs can be searched and viewed on the web front end where you can see:
   * The Test ID
   * Time & Date
   * Engineer
   * Upload Speed
   * Download Speed
   * Peak Speed
   * Upsteam MAC Address
   * A link to the raw JSON test file

Below you can see the odroid performing the test 

  ![alt text](https://github.com/GuillermoElectrico/hyperspeed-tester/blob/master/Documentation/Pictures/Tester.gif "")

  ![alt text](https://github.com/GuillermoElectrico/hyperspeed-tester/blob/master/Documentation/Pictures/Screen_Output%20.jpg "")
  
And the front end!

  ![alt text](https://github.com/GuillermoElectrico/hyperspeed-tester/blob/master/Documentation/Pictures/lintester_php.PNG "")
  
  ![alt text](https://github.com/GuillermoElectrico/hyperspeed-tester/blob/master/Documentation/Pictures/lintester_admin_php.PNG "")
