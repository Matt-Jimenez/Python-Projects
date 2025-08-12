"""
Graph usage dashboard.

Collects usage statistics from Microsoft Graph and produces a bar chart and Excel report.
"""

import pandas as pd
import matplotlib.pyplot as plt
from O365 import Account

# Replace with your Azure AD app credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'


def authenticate():
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/.default'])
    return account


def gather_counts():
    account = authenticate()
    data = {}
    mailbox = account.mailbox()
    data['Emails'] = mailbox.inbox_folder().total_count
    schedule = account.schedule()
    calendar = schedule.get_default_calendar()
    data['Events'] = len(list(calendar.get_events(limit=100)))
    onedrive = account.storage()
    drive = onedrive.get_default_drive()
    data['Files'] = len(list(drive.get_items(limit=100)))
    return data


def build_dashboard():
    counts = gather_counts()
    df = pd.DataFrame(list(counts.items()), columns=['Resource', 'Count'])
    df.plot(kind='bar', x='Resource', y='Count', legend=False)
    plt.title('Microsoft 365 Usage')
    plt.tight_layout()
    plt.savefig('dashboard.png')
    # Write to Excel
    df.to_excel('usage.xlsx', index=False)


if __name__ == '__main__':
    build_dashboard()