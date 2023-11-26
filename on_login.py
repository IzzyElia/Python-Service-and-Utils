# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import TestNotification as Notifier
import last_release_checker
from notifier import send_local_notification

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

def show_new_releases():
    new_releases = last_release_checker.check_new_releases()
    if (new_releases):
        notification = ""
        for release in new_releases:
            notification += f'{release["artist"]} by {release["artist"]}\n'
        send_local_notification("New Releases", notification)
        print("New Releases", notification)
        last_release_checker.update_log(new_releases)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Izzy')

    print("Getting new releases...")
    show_new_releases()
