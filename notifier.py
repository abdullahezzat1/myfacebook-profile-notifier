import time
from os import path
import subprocess


def notify(summary: str, body: str):
    return subprocess.call(
        [
            'notify-send',  # notification program name
            '-a', 'Facebook Notifier',  # Sender name...?
            summary,  # Message summary
            body  # Message body
        ]
    )
# add icon to notification


def notify_list(notification_list):
    for notification in notification_list:
        notify(notification['profile_name'],
               notification['post_title'] + '\n ' + notification['post_time'])
    print('Successfully received notifications at ' + time.asctime())
