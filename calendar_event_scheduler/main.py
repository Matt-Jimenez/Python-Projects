"""
Calendar event scheduler.

Reads events from a CSV file and schedules them in an Outlook calendar using the O365 library.
"""

import pandas as pd
from O365 import Account
from datetime import datetime
import pytz

# Replace with your Azure AD app credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'


def authenticate():
    """Authenticate and return an O365 account."""
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/Calendars.ReadWrite'])
    return account


def schedule_events():
    """Read events.csv and create calendar events."""
    df = pd.read_csv('events.csv')
    account = authenticate()
    schedule = account.schedule()
    calendar = schedule.get_default_calendar()
    local_tz = pytz.timezone('UTC')
    for _, row in df.iterrows():
        event = calendar.new_event()
        event.subject = row['subject']
        # Convert ISO strings to datetime with timezone
        start = local_tz.localize(datetime.fromisoformat(row['start']))
        end = local_tz.localize(datetime.fromisoformat(row['end']))
        event.start = start
        event.end = end
        attendees = [att.strip() for att in str(row['attendees']).split(';') if att]
        for email in attendees:
            event.attendees.add(email)
        event.save()


if __name__ == '__main__':
    schedule_events()