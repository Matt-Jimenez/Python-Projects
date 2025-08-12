"""
Outlook email parser.

Authenticates to an Outlook mailbox using O365, filters messages, and downloads attachments to a local folder.
"""

import os
from O365 import Account

# Replace with your Azure AD app credentials
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'

DOWNLOAD_FOLDER = 'attachments'


def authenticate():
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/Mail.Read'])
    return account


def parse_mailbox():
    """Scan the mailbox, filter messages, and download attachments."""
    account = authenticate()
    mailbox = account.mailbox()
    inbox = mailbox.inbox_folder()
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    for message in inbox.get_messages(limit=50):
        # Example filter: subject contains 'Report'
        if 'Report' in message.subject:
            for attachment in message.attachments:
                save_path = os.path.join(DOWNLOAD_FOLDER, attachment.name)
                attachment.save(save_path)
            print(f'Saved attachments from: {message.subject}')


if __name__ == '__main__':
    parse_mailbox()