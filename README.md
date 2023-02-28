# TridotZwiftDownloader
Python - Selenium script which downloads the days zwo file from tridot website

This script is created to solve my own personal need. I wanted my zwift workouts to be downloaded and placed in the workouts directory
Each day before working out, without having to go through the multiple clicks on the tridot interface

This script will connect to tridot using credentials you save in the conf file
Check if the days workout contains a bike session
if it does, it will download the ZWO file and place it in the workouts directory per the conf file

It will download the file with a static filename and overwrite any prior days workout file (This keeps from filling the workouts folder with old rides)

This works on my machine, in my environment. your mileage may vary. That's Windows 11, Python 3.11

HOW TO INSTALL

1. Ensure you have Chrome Installed
2. Ensure you have downloaded the matching version of the chromedriver.exe to match the version of chrome you installed
https://chromedriver.chromium.org/downloads

3. Ensure you have python installed
4. pip install selenium and cryptography
5. make a directory for the scripts to live in (i.e. C:\Toolbox\Tridot\ ) 
6. copy the two PY scripts to that directory
7. run python c:\toolbox\tridot\GenEncryptedPassword.py

  You will be prompted for and need to know the answers to these:  
  TRIDOT USERNAME - i.e. myemail@email.com
  TRIDOT PASSWORD - i.e. MyPassword1!
  PATH TO THE WEBDRIVER (INCLUDING THE EXE NAME ) - i.e. C:\Toolbox\chromedriver.exe 
  PATH TO YOUR ZWIFT WORKOUTS FOLDER - i.e. C:\Users\{userid}\Documents\Zwift\Workouts\#######

8. This will generate a tridot.ini file . You can change the tridot.ini once created, however you'll need to use this tool if your password has changed or you entered it incorrectly above. 

9. Run/schedule python TridotZwoDownloader.py 

The script will connect to tridot, check if you have a bike workout scheduled for the day. If so, it will download the ZWO and copy it into the Workouts folder with the name "Todays_Tridot_Workout.zwo" 



