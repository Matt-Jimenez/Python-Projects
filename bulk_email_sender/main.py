"""
Bulk email sender using Microsoft Graph.

This script authenticates using O365, reads recipient data from an Excel file, and sends personalised email messages.
"""

import pandas as pd
from O365 import Account

# Replace with your Azure AD app credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'


def get_account():
    """Authenticate and return an O365 account object."""
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/Mail.Send'])
    return account


def send_bulk_emails():
    """Send personalised emails to recipients defined in recipients.xlsx."""
    account = get_account()
    mailbox = account.mailbox()
    df = pd.read_excel('recipients.xlsx')
    for _, row in df.iterrows():
        message = mailbox.new_message()
        message.to.add(row['email'])
        message.subject = f"Hello {row['name']}"
        message.body = f"Dear {row['name']},\n\nThis is a sample message."
        message.send()


if __name__ == '__main__':
    send_bulk_emails()