# TridotZwiftDownloader
Python - Selenium script which downloads the days zwo file from tridot website

This script is created to solve my own personal need. I wanted my zwift workouts to be downloaded and placed in the workouts directory
Each day before working out, without having to go through the multiple clicks on the tridot interface

This script will connect to tridot using credentials you save in the conf file
Check if the days workout contains a bike session
if it does, it will download the ZWO file and place it in the workouts directory per the conf file

It will download the file with a static filename and overwrite any prior days workout file (This keeps from filling the workouts folder with old rides)

This works on my machine, in my environment. your mileage may vary

