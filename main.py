import datetime
import time
import notifier
import last_release_checker


def seconds_until(specified_time):
    """
    This function calculates the number of seconds from now until the specified time.

    Args:
    specified_time (str): The specified time in the format 'HH:MM:SS'

    Returns:
    int: The number of seconds until the specified time
    """

    # Current time
    now = datetime.datetime.now()

    # Specified time for today
    specified_time_today = datetime.datetime.strptime(specified_time, '%H:%M:%S').replace(
        year=now.year, month=now.month, day=now.day
    )

    # If the specified time is already past for today, calculate the time for the next day
    if specified_time_today < now:
        specified_time_today += datetime.timedelta(days=1)

    # Calculate the difference in seconds
    delta = specified_time_today - now
    return int(delta.total_seconds())


def show_new_releases():
    new_releases = last_release_checker.check_new_releases()
    if (new_releases):
        notification = ""

        for release in new_releases:
            notification += f'{release["artist"]} by {release["artist"]}\n'
        notifier.send_pushover_notification("New Releases: \n" + notification)
        print("New Releases", notification)
        last_release_checker.update_log(new_releases)
    else:
        notifier.send_pushover_notification("No new releases today")


def run_cycle():
    show_new_releases()


if __name__ == "__main__":
    while True:
        time_until_run = seconds_until("14:00:00")
        print (f'Running in {time_until_run} seconds')
        time.sleep(time_until_run)
        run_cycle()