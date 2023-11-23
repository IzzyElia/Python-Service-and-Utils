import subprocess
import platform
import requests

def send_pushover_notification(message):
    auth_details = {}
    with open('pushover-auth.txt', 'r') as file:
        for line in file:
            if ':' in line:
                item, value = line.strip().split(':', 1)
                auth_details[item] = value

    payload = {
        'token': auth_details['api_token'],
        'user': auth_details['user_key'],
        'message': message
    }
    response = requests.post('https://api.pushover.net/1/messages.json', data=payload)
    if response.status_code == 200:
        print(f'Notification sent successfully - {message}')
    else:
        print('Failed to send notification.')
    return response.status_code



def send_local_notification(title, message):
    """Sends a notification on Windows, macOS, or Linux."""
    os_name = platform.system()

    if os_name == "Darwin":  # macOS
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(["osascript", "-e", script])
    elif os_name == "Windows":
        print("No windows support yet")
    elif os_name == "Linux":
        subprocess.run(["notify-send", title, message])
    else:
        print("Unsupported operating system for notifications.")

if __name__ == "__main__":
    # Example usage
    send_local_notification("Test Title", "This is a test notification.")
