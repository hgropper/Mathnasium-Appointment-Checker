# Mathnasium-Appointment-Checker
At all times students have a certain number of remaining sessions left. Mathnasium does not have an automatic system to let the parents know that their kids are running low on sessions. How could we easily pull the data from the scheduling website to access this data, so then we can notify the parents ourselves?

## The task
To get each student's remaining number of sessions.

## Why was this important?
IF the number of session's are low we can notify the parents to purchase more sessions.

## Problem!
If we were to do this process manually, then it would take a really long time. [Acuity](https://www.acuityscheduling.com/) has a unique way of figuring out how many sessions a student has left. For each student we would have to click various times and wait for multiple webpages to load. This task is very tedious and takes too much time.

## Solution
Utilizing the requests module from python I can analyze the HTTP requests, login to the service, and pull all the necessary data automagically.

# Description
Please install the necessary modules/packages below in your command prompt by typing in the commands below.
If you do not have pip installed please install it here: https://pip.pypa.io/en/stable/installation/

requests - pip install requests
time - pip install time
datetime - pip install datetime
bs4 - pip install bs4
re - pip install re

Enjoy!

And... yes this program was tested and successfully put to use in the workplace. 
