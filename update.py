#!/usr/bin/env python3
import os
import shutil
import subprocess

# Function to run shell commands
def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error running command '{command}': {stderr.decode().strip()}")
    return stdout.decode().strip()

# Function to read ignore paths from the config file
def read_ignore_paths(config_file):
    ignore_paths = []
    with open(config_file, 'r') as file:
        for line in file:
            if line.startswith('ignore'):
                _, path = line.split(maxsplit=1)
                ignore_paths.append(path.strip())
    return ignore_paths

# Function to clear directory with ignore paths
def clear_directory(directory, ignore_paths):
    # Change to the directory
    os.chdir(directory)
    # List all files and directories
    for item in os.listdir(directory):
        if item == os.path.basename(__file__) or item in ignore_paths or item == os.path.basename(config_file):
            # Skip the script file itself and ignored paths
            continue
        if os.path.isdir(item):
            # Recursively remove directories
            shutil.rmtree(item)
        else:
            # Remove files
            os.remove(item)

# Function to clone the git repository
def clone_repository(repo_url, directory):
    run_command(f'git clone {repo_url} {directory}')

# Main function

if __name__ == "__main__":
    if input('Running this script will delete and rebuild the app, '
             'except for files listed in update_config.txt. YES to continue') == 'YES':
        script_directory = os.path.dirname(os.path.realpath(__file__))
        git_repository_url = 'https://github.com/IzzyElia/Python-Service-and-Utils.git'
        config_file = 'update_config.txt'  # Config file with ignore paths

        ignore_paths = read_ignore_paths(config_file)

        print(f"Clearing the directory: {script_directory}")
        clear_directory(script_directory, ignore_paths)

        print(f"Cloning repository into {script_directory}")
        clone_repository(git_repository_url, script_directory)

        print("Operation completed successfully.")
