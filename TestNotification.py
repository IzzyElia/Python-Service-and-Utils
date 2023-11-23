# Filename: notification_module.py
import os
from datetime import datetime

def show_notification():
    """Shows a notification with the current date and time."""
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    apple_script_command = f'''
    osascript -e 'display notification "Current Date and Time: {current_date}" with title "Login Notification"'
    '''
    os.system(apple_script_command)

if __name__ == "__main__":
    show_notification()
