# always generating a readme file at start (overwriting if it exists)
file = open("README.txt", 'w')
file.write("Please install the necessary modules/packages below in your command prompt by typing in the commands below.\n")
file.write("If you do not have pip installed please install it here: https://pip.pypa.io/en/stable/installation/" + "\n\n")
module_imports = (
"requests - pip install requests\n" +  
"time - pip install time\n" +
"datetime - pip install datetime\n" +
"bs4 - pip install bs4\n" +
"re - pip install re")
file.write(module_imports + "\n\n")
file.write("Enjoy!")
file.close()

import requests # to access, login, the acuity website
import time # for time delay
from datetime import date # to found the current time and compare it to others
from bs4 import BeautifulSoup
import re # regular expressions
import random

# if any of the modules are not installed
# please install this in the terminal

def log(string):
    '''
    Creates a function to log all the needed information
    Prints and logs information to the log.txt file with todays date
    '''
    
    # opening, writing, and closing the file
    file = open(str(date.today().strftime("%B %d, %Y").replace(",","").replace(" ","-")) + '-log.txt', 'a+')
    file.write(string + "\n")
    file.close()
    
    # we also print a string of the information that was saved to the console
    print(string)
    
def error(error_message):
    '''Ends the program after 15 seconds if there is an error'''
    log(error_message)
    log("Ending program in 15 seconds.")
    time.sleep(15)
    exit()
    
def read_config():
    """
    Attempts to read out config file
    to grab the username and password to sign 
    into the website. If this fails, we will present
    an error code and the program will stop.
    
    If successful we return the supplemented username
    as password of the user.
    """
    try:
        file = open('config.txt','r')
    except Exception as FileNotFoundError:
        log("The config file has not been created.")
        log("Creating the config file...")
        
        # creating our config file
        file = open('config.txt','w')
        
        log("config.txt file successfully created!")
        log("Please enter credentials to access the website.")
        log("This information will be saved in the config file.")
        username = input("Username: ")
        password = input("Password: ")
        
        # writing credentials
        with open('config.txt', 'w') as f:
            f.write("Username: " + username + "\n" + "Password: " + password)
            
        log("config.text successfully saved with new credentials.")
        
        # for accessing our data
        file = open('config.txt','r')
        
    try:
        # getting the data of the config file
        data = file.readlines()

        login_information = []
        for credentials in data:
            login_information.append(credentials.split(":")[1].strip())

        # we return a tuple, so this information remains unmodified
        log("Detected username: " + str(login_information[0]))
        log("Detected password: " + str(login_information[1]))
        
    except Exception as e:
        log("Error reading the config file. " + str(e))
        log("Please delete the config file and try again.")
        error("Could not read the credentials of the config file.")
        
    log("Successfully read user credentials from config.txt file.")
    file.close()
    return tuple(login_information)
  
  initial_url = "https://secure.acuityscheduling.com/login.php?nav=1&btn=nav-bar"

session = requests.Session() # creating a user session

# this hides the fact that we are a both interacting with the website
# this will 
headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}


try:
    website_response = session.get(initial_url) # storing our response 
except:
    error("Could not load the initial webpage.")

# let's check to see we successfully connected to the webiste
if (website_response.ok == False):
    error("Failed to connect to the website.\n" +
          "HTTP Error Code: " + str(website_response.status_code))
else:
    log("Successfully connected to " + initial_url.split("?nav")[0] +
       " with status code " + str(website_response.status_code))
    
# let's check to see that the html format of the website has not changed
html = BeautifulSoup(website_response.content)

random_html_container = str(html.find("input"))
html_container = ''

# checks to make sure the input container html has not changed
if random_html_container != html_container:
    error("The website HTML code has changed.\nPlease contact Mr. Harrison to update the code.")
else:
    log("Website input check successful.")
    
    
username, password = read_config()

# sending our username to the server
username_auth_url = "https://secure.acuityscheduling.com/oauth2/user-type"

# creating new headers to pass website security (username)
headers = {
    "authority": "secure.acuityscheduling.com",
    "method": "POST",
    "path": "/oauth2/user-type",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "35",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://secure.acuityscheduling.com",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

try:
    payload = {"email": username}
    website_response = session.post(username_auth_url, headers = headers, data = payload, timeout = 10)
except:
    error("Timeout error, could not submit email. Please restart the program and try again.")

if (website_response.ok == False):
    error("Failed to send the username to the website. Login failed. \n" +
          "HTTP Error Code: " + str(website_response.status_code))
else:
    log("Successfully sent the username " + initial_url.split("?nav")[0] +
       " with status code " + str(website_response.status_code))
    
    
# sending our password to the server
password_auth_url = "https://secure.acuityscheduling.com/login.php?nav=1&btn=nav-bar"

# creating new headers to pass website security (password)
headers = {
    "authority": "secure.acuityscheduling.com",
    "method": "POST",
    "path": "/login.php?nav=1&btn=nav-bar",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "92",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://secure.acuityscheduling.com",
    "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest"
}

try:
    payload = {"username": username,
               "password": password,
               "locale": "en-US",
               "login": "Log in"}
    website_response = session.post(password_auth_url, headers = headers, data = payload, timeout = 10)
except:
    error("Timeout error, could not submit email. Please restart the program and try again.")

if (website_response.ok == False):
    error("Failed to send the password to the website. Login Failed.\n" +
          "HTTP Error Code: " + str(website_response.status_code))
else:
    log("Successfully sent the password " + initial_url.split("?nav")[0] +
       " with status code " + str(website_response.status_code))
    log("Login successful!")
    
    
log("Starting to verify the website's identity.")
html = str(BeautifulSoup(website_response.content).text.strip())
string_verify = "Today's Appointments"

if string_verify not in html:
    log("You might have entered the wrong credentials.")
    error("Could not verify the webpages identity.")
else:
    log("Verification successful!")
    
    
log("Attempting to access the client page.")
client_url = "https://secure.acuityscheduling.com/clients.php"

try:
    website_response = session.get(client_url)  
except:
    error("Failed to access the client page.")
    
html = str(BeautifulSoup(website_response.content))
string_verify = "Client List"

if string_verify not in html or website_response.ok == False:
    error("Did not access the correct client page.")
else:
    log("Attempt successful!")
    
# raw html content
html = BeautifulSoup(website_response.content)

try:
    payload_dictionary = dict() # to hold all the values that would be needed to create a payload
    # each element in the list contains data about the student and a link to the number of
    # up coming sessions
    ordered_lists = html.findAll("li")  

    students_detected = len(html.findAll("li"))

    # we iterate through the ordered_lists and we find information about...
    # students name
    # upcoming sessions
    log("Number of students detected: " + str(students_detected))
    log("Creating payloads for every student...")
    # for the payload...
    # note we need to find the ecd code which is hidden in another URL in the html webpage
    upcoming_sessions_url = "https://secure.acuityscheduling.com/clients.php?action=detail&ecd="
    for batch in ordered_lists:
        
        # getting the students name and phone number
        try:
            client_name = batch.find("span","client-name").text
        except:
            client_name = 'unknown'

        try:
            client_phone = batch.find("span","client-phone").text
        except:
            client_phone = 'unknown'

        # finding the hidden ecd code for our paylaod
        first_link = batch.findAll("a")[1]['href']
        hidden_index = first_link.index('ecd')
        ecd_link = first_link[hidden_index:].replace("ecd=","")
        ecd_code = ecd_link.split("%")[0]

        # building the second link
        # the one we are going to request
        second_link = upcoming_sessions_url + ecd_link

        # now that we have the link, let's build the payload
        payload = {
            "action": "detail",
            "ecd": ecd_code + "==",
            "backto": "clients"
        }

        # the last component is the header
        # to fool the website we are not a robot

        header = {
            "authority": "secure.acuityscheduling.com",
            "method": "GET",
            "path": ("/clients.php?action=detail&ecd=" + ecd_link), 
            "scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "sec-ch-ua-mobile": '?0',
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": 'navigate',
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
        }

        # adding the payload to the payload dictionary
        payload_dictionary[client_name] = [second_link, header, payload, client_name]

    log("Successfully created all payloads!")

except Exception as e:
    error("Could not create payloads. Error: " + str(e))
    
# deleting extra user accounts we do not want to scan
users_to_block = ['IT, BLOCK']
for user in users_to_block:
    try:
        del payload_dictionary[user]
    except:
        pass
      
student_upcoming_appointments_dict = dict() # holds information about we has what appointments left
# sending the payloads and getting upcoming sessions
# timing the time it takes to scan
start = time.time()
for student in payload_dictionary:
    
    # random delay so we do not get IP blocked
    time.sleep(random.randint(1,10)/50)
    
    try:
        payload_list = payload_dictionary[student]
        client_name = payload_list[-1]
        website_response = session.post(payload_list[0], headers = payload_list[1], data = payload_list[2], timeout = 10)
        html_code = BeautifulSoup(website_response.content, "html.parser")
        canceled_count = len(html_code.findAll("div",{"class":"content client-extra-details client-appt-history"})[0].findAll("div",{"class":"appointment-item is-canceled"}))
        upcoming_appts_string = [x for x in html_code.findAll("h3") if "Upcoming Appointments" in x.text][0].text
        
        # getting number of appointments using regex
        try:
            # UPDATING FOR CANCELED APPOITMENTS HERE
            number_of_appointments = int(re.findall("[0-9]+",upcoming_appts_string)[0]) - canceled_count
        except:
            number_of_appointments = 0
            
        # THRESHOLD (FLAGS) FOR OUTPUTING NUMBER OF APPOINTMENTS
        if number_of_appointments < 5 or True:
            log("Scanned: " + client_name + " Upcoming Appointments(" + str(number_of_appointments) + ")" + ", " + str(canceled_count) + " canceled appointments.")
            student_upcoming_appointments_dict[client_name] = number_of_appointments # adding data to dictionary
    except Exception as e:
        log("Failed to get information for " + client_name)
        log("Program is sleeping for 5 seconds to wait for better internet OR there might be another error.")
        log("CURRENT ERROR: " + str(e))
        
        # if we have already not rescanned for the student
        if list(payload_dictionary.keys()).count(student) < 2:
            payload_dictionary.append(student) # add the student back for a rescan
        else:
            log("COULD NOT SCAN STUDENT: " + student + " on second attempt.")
            
        time.sleep(5) # small delay because connection was probably interrupted 
    
end = time.time()
log("Scan successful!")
log(f"Scan time period {round((end-start)/60,2)} minutes.")
log("Finished Scan!")
