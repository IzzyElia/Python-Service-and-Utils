#!/usr/bin/env python3
import os
import subprocess

# Function to run shell commands
def run_command(command):
    process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        print(f"Error running command '{command}': {process.stderr}")
        exit(process.returncode)
    return process.stdout.strip()

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
run_command('eval "$(ssh-agent -s)"')
run_command(f'ssh-add "{ssh_key_path}"')

# Prompt for Spotify Client ID and Secret
spotify_client_id = input("Please enter your Spotify Client ID: ")
spotify_secret = input("Please enter your Spotify Secret Key: ")

# Set environment variables for Spotify
bashrc_path = os.path.expanduser('~/.bashrc')
with open(bashrc_path, 'a') as bashrc:
    bashrc.write(f'\n# Spotify API credentials\n')
    bashrc.write(f'export SPOTIFY_CLIENT_ID="{spotify_client_id}"\n')
    bashrc.write(f'export SPOTIFY_SECRET="{spotify_secret}"\n')

print("Spotify Client ID and Secret Key have been set as environment variables.")

# Reminder to source .bashrc
print(f"Please run 'source {bashrc_path}' to load the new environment variables or restart the terminal session.")
