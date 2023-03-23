from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from cryptography.fernet import Fernet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jsonobject import *
import configparser
import os
import time
import shutil
import os

# TODO 
#  - MAX WAIT TIME OF 5MIN should come from ini
#  - Figure out how to make it work headless
#  - Figure out how to make it work set GPS coordinates from INI
#  - Figure out if it works with 2 workouts on the same day or not

# Get where the script lives
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# Define the folder path to delete and recreate
tmp_folder_path = os.path.join(script_dir,"temp")

# Delete the folder and all its contents
shutil.rmtree(tmp_folder_path)

# Recreate the folder
os.makedirs(tmp_folder_path)

# Load configuration file
config = configparser.ConfigParser()
config.read('Tridot.ini')

# Get username from config file
username = config.get('Tridot', 'username')

# Get encrypted password from config file
encrypted_password = config.get('Tridot', 'password')

# Home URL
login_url = config.get('Tridot','Login_URL')

# Decrypt password
key = config.get('Tridot', 'key')
f = Fernet(key)
password = f.decrypt(encrypted_password.encode()).decode()

# Get the path to the webdrive
webdriver_path = config.get('Tridot','WebDriverPath')

# Get the workout filename
WorkoutDir = config.get('Tridot','WorkoutDir')

# Get location info
Latitude = config.get('Tridot','latitude')
Longitude = config.get('Tridot','longitude')

# Set the path to the log file
log_path = "webdriver.log"

# Set the debug mode
Debug_String = config.get('Tridot','Debug')
Debug = False
if Debug_String.lower() == 'true':
    Debug = True
else:
    Debug = False
  
# Create a ChromeOptions object with headless mode enabled
chrome_options = Options() 
chrome_options.add_argument('--window-size=1920x1080')

if not Debug:
    chrome_options.add_argument("--headless")

prefs = {
    'profile.default_content_setting_values.notifications': 1,
    'profile.managed_default_content_settings.geolocation': 1,
    "profile.default_content_settings.popups": 0,    
    "download.default_directory": tmp_folder_path,  
    "download.prompt_for_download": False, 
    "download.directory_upgrade": True
}

chrome_options.add_experimental_option('prefs', prefs)


# Create a new instance of the ChromeDriver with ChromeOptions
browser_driver = webdriver.Chrome(executable_path=webdriver_path, options=chrome_options)
browser_driver.maximize_window()

# Navigate to Tridot website
browser_driver.get(login_url)

# Enter username and password
username_input = browser_driver.find_element_by_id("exampleInputusername1")
password_input = browser_driver.find_element_by_id("exampleInputpassword1")
username_input.send_keys(username)
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)


# Wait for post-login page to load
wait = WebDriverWait(browser_driver, 15)

# Wait for Hamburger Menu
HamburgerMenu = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".nucleo-icon.icon-menu-3-1")))

# Check to see if there's a bike workout for today
elements = browser_driver.find_elements_by_class_name("session-type-icon")

# Loop through the elements and check if the src attribute contains 'bike'
for element in elements:
    if 'bike' in element.get_attribute('src'):
        # Click the bike icon
        element.click() 
        
        # Click the Hamburger Menu
        HamburgerMenu.click()        
        
        # Click Download option
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".icon-data-download-1"))).click()
        # Click ZWO option
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'label[btnradio="ZWO"]'))).click()

        # Click Export Session
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".export-btn"))).click()

        # Wait for download to finish
        start_time = time.time()
        while True:
            # Check if the folder contains a single file
            files = os.listdir(tmp_folder_path)
            if len(files) == 1:
                file_path = os.path.join(tmp_folder_path, files[0])
                
                # Check if the file ends with .crdownload
                if file_path.endswith(".crdownload"):
                    # Check if the download is complete
                    if time.time() - os.path.getmtime(file_path) > 300:
                        raise Exception("Gave up trying to download")
                    else:
                        time.sleep(1)
                        continue
                
                # File is downloaded successfully
                break
            
            # Check if we have waited for more than 5 minutes
            if time.time() - start_time > 300:
                raise Exception("Gave up trying to download")
            
            # Wait for 1 second before checking again
            time.sleep(1)

        # Rename the downloaded file to the desired filename
        downloaded_filename = os.listdir(tmp_folder_path)[0]
        new_filename = os.path.join(WorkoutDir,'Todays_Tridot_Workout.zwo')  # Replace with your desired filename
        if os.path.exists(new_filename):
            os.remove(new_filename)  # Delete existing file

        os.rename(os.path.join(tmp_folder_path, downloaded_filename),
                new_filename)

# Close the browser window
browser_driver.close()
# Quit browser
browser_driver.quit()
