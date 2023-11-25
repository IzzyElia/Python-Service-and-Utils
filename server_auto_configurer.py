#!/usr/bin/env python3
import os
import subprocess
import sys

# Function to run shell commands
def run_command(command, print_output=True):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        if print_output:
            print(process.stdout)
    else:
        print(f"Error running command '{command}': {process.stderr}")
        exit(process.returncode)
    return process.stdout.strip()

# Function to check and install python-dotenv if not already installed
def check_and_install_dotenv():
    try:
        import dotenv
    except ImportError:
        print("python-dotenv not found, installing it now...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'python-dotenv'], check=True)
        import dotenv  # Import after installing


# Now we call the function to make sure python-dotenv is installed
check_and_install_dotenv()

# Check for existing SSH keys
ssh_dir = os.path.expanduser('~/.ssh')
if not os.path.exists(ssh_dir):
    os.makedirs(ssh_dir)
ssh_key_path = os.path.join(ssh_dir, 'id_ed25519')

if not os.path.exists(ssh_key_path):
    print("No SSH key found, generating a new SSH key...")
    email = input("Please enter your email address for SSH key: ")
    run_command(f'ssh-keygen -t ed25519 -C "{email}" -f "{ssh_key_path}" -N ""')

# Start the ssh-agent and add the key
print("Starting the ssh-agent...")
run_command('eval "$(ssh-agent -s)"', print_output=True)
run_command(f'ssh-add "{ssh_key_path}"', print_output=True)

# Prompt for Spotify Client ID and Secret
spotify_client_id = input("Please enter your Spotify Client ID: ")
spotify_secret = input("Please enter your Spotify Secret Key: ")

# Set environment variables for Spotify in a local .env file
env_file_path = '.env'  # You can specify a path to the .env file if needed

# Check if .env file exists, if not, create it
if not os.path.exists(env_file_path):
    open(env_file_path, 'a').close()

def write_env_variables(path, spotify_client_id, spotify_secret):
    # Read the current lines from the .env file
    if os.path.exists(path):
        with open(path, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    # Create a dictionary to hold the current environment variables
    env_vars = {line.split('=')[0]: line for line in lines if '=' in line}

    # Update the dictionary with the new values
    env_vars['SPOTIFY_CLIENT_ID'] = f'SPOTIFY_CLIENT_ID="{spotify_client_id}"\n'
    env_vars['SPOTIFY_SECRET'] = f'SPOTIFY_SECRET="{spotify_secret}"\n'

    # Write the updated values back to the .env file
    with open(path, 'w') as file:
        for key in env_vars:
            file.write(env_vars[key])

write_env_variables(env_file_path, spotify_client_id, spotify_secret)

print("Spotify Client ID and Secret Key have been added to the .env file.")

# After generating the SSH key, output the public key contents to the user
with open(f"{ssh_key_path}.pub", 'r') as public_key_file:
    public_key = public_key_file.read()
    print("Your public SSH key is:\n")
    print(public_key)
    print("\n")

# Reminder to load the .env file in their development environment
print(f"Please ensure that your development environment is set up to load variables from {env_file_path}.")
