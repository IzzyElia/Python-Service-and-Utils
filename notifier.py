import subprocess
import platform
import requests
import os
from dotenv import load_dotenv

def send_pushover_notification(message):
    load_dotenv()

    try:
        pushover_api_token = os.environ['PUSHOVER_API_TOKEN']
    except KeyError:
        raise KeyError("Environment variable 'PUSHOVER_API_TOKEN' is not set")
    try:
        pushover_user_key = os.environ['PUSHOVER_USER_KEY']
    except KeyError:
        raise KeyError("Environment variable 'PUSHOVER_USER_KEY' is not set")

    payload = {
        'token': pushover_api_token,
        'user': pushover_user_key,
        'message': message
    }
    response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    if response.status_code == 200:
        print(f'Notification sent successfully - {message}')
    else:
        print(f'Failed to send notification: {response.text}')
    return response.status_code



def send_local_notification(title, message):
    """Sends a notification on Windows, macOS, or Linux."""
    os_name = platform.system()

    if os_name == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    else:
        print("Unsupported operating system for local notifications.")

if __name__ == "__main__":
    # Example usage
    send_pushover_notification("Test notification")
    send_local_notification("Test Title", "This is a test notification.")
