from cryptography.fernet import Fernet
import getpass
import configparser

# Prompt user for username
username = input("Username: ")

# Prompt user for password
password = getpass.getpass(prompt='Password: ')

# Generate encryption key
key = Fernet.generate_key()

# Encrypt password
f = Fernet(key)
encrypted_password = f.encrypt(password.encode()).decode()

# Prompt for webdriver location
WebDriver = input("Enter complete path to webdriver: ")

# Prompt for ZWO workout folder and filename
ZWOPath = input("Enter the complete path to where your workouts folder is: ")

# Write out config file
config = configparser.ConfigParser()
config['Tridot'] = {
    'username': username,
    'password': encrypted_password,
    'key': key.decode(),
    'WebDriverPath': WebDriver,
    'WorkoutDir': ZWOPath
}

with open('Tridot.ini', 'w') as configfile:
    config.write(configfile)
