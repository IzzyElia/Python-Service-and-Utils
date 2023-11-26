#!/usr/bin/env python3
import os
import subprocess
from crontab import CronTab


# Function to run shell commands
def run_command(command, print_output=True):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        if print_output:
            print(process.stdout)
    else:
        print(f"Error running command '{command}': {process.stdout} {process.stderr}")
        exit(process.returncode)
    return process.stdout.strip()


# Function to ensure python3-venv is installed
def install_python_venv():
    install_command = 'sudo apt-get update && sudo apt-get install -y python3-venv'
    run_command(install_command)


#Check if variable exists among the environment variables
def check_env_variable_written(path, variable_name):
    # Read the current lines from the .env file
    if os.path.exists(path):
        with open(path, 'r') as file:
            lines = file.readlines()
    else:
        return False # No environment variable file, so the value has definitely not been written

    # Create a dictionary to hold the current environment variables
    env_vars = {line.split('=')[0]: line for line in lines if '=' in line}

    return variable_name in env_vars.keys()

def write_env_variable(path, variable_name, variable_value):
    # Read the current lines from the .env file
    if os.path.exists(path):
        with open(path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    # Create a dictionary to hold the current environment variables
    env_vars = {line.split('=')[0]: line for line in lines if '=' in line}

    # Update the dictionary with the new values
    env_vars[variable_name] = f'{variable_name}="{variable_value}"\n'

    # Write the updated values back to the .env file
    with open(path, 'w') as file:
        for key in env_vars:
            file.write(env_vars[key])


def set_spotify_authentication():
    spotify_client_id = input("Please enter your Spotify Client ID: ")
    spotify_secret = input("Please enter your Spotify Secret Key: ")
    write_env_variable(env_file_path, 'SPOTIFY_CLIENT_ID', spotify_client_id)
    write_env_variable(env_file_path, 'SPOTIFY_SECRET', spotify_secret)
    print("Spotify Client ID and Secret Key have been added to the .env file.")

def set_pushover_authentication():
    pushover_user_key = input("Please enter your Pushover User Key: ")
    pushover_api_token = input("Please enter your Pushover API Token: ")
    write_env_variable(env_file_path, 'PUSHOVER_API_TOKEN', pushover_api_token)
    write_env_variable(env_file_path, 'PUSHOVER_USER_KEY', pushover_user_key)
    print("Pushover API Token has been added to the .env file.")


# Make sure python3-venv is installed
if os.name == "Linux":
    install_python_venv()

# Set up the virtual environment and enter it
print('Setting up the virtual environment...')
run_command('python3 -m venv venv')
run_command('venv/bin/python -m pip install -r requirements.txt')

print('setting up the scheduler...')
# Access the current user's cron tab
cron = CronTab(user='root')
# Find the job and remove it
job = cron.new(command='echo hello_world')
cron.write()


# Set environment variables for Spotify in a local .env file
env_file_path = '.env'  # You can specify a path to the .env file if needed

# Check if .env file exists, if not, create it
if not os.path.exists(env_file_path):
    open(env_file_path, 'a').close()

if check_env_variable_written(env_file_path, 'SPOTIFY_CLIENT_ID') or check_env_variable_written(env_file_path, 'SPOTIFY_SECRET'):
    if input('Spotify authentication information found. Update it? (y/n)').lower() == 'y':
        set_spotify_authentication()
else:
    set_spotify_authentication()

if check_env_variable_written(env_file_path, 'PUSHOVER_API_TOKEN'):
    if input('Pushover API information found. Update it? (y/n)').lower() == 'y':
        set_pushover_authentication()
else:
    set_pushover_authentication()


print("Script unscheduled")


# Output the public ssh key contents to the user to they can quickly copy them
#with open(f"{ssh_key_path}.pub", 'r') as public_key_file:
#    public_key = public_key_file.read()
#    print("Your public SSH key is:\n")
#    print(public_key)


# Reminder to load the .env file in their development environment
print(f"REMINDER: Please ensure that your development environment is set up to load variables from {env_file_path}.")
print(f"REMINDER: Enter the virtual environment with: source venv/bin/activate")
