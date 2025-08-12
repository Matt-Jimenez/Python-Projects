"""
Teams chat automation script.

Authenticates with Microsoft Graph via O365 and posts messages from a text file to a Teams channel or chat.
"""

import time
from O365 import Account

# Replace with your Azure AD app credentials and channel ID
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
TEAM_ID = 'your_team_id'
CHANNEL_ID = 'your_channel_id'


def authenticate():
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/.default'])
    return account


def post_messages():
    """Post each line from messages.txt to the Teams channel."""
    account = authenticate()
    with open('messages.txt', 'r') as f:
        for line in f:
            message = line.strip()
            if not message:
                continue
            endpoint = f'/teams/{TEAM_ID}/channels/{CHANNEL_ID}/messages'
            data = {
                'body': {
                    'content': message
                }
            }
            account.graph_client.post(endpoint, data=data)
            print(f'Posted message: {message}')
            time.sleep(1)


if __name__ == '__main__':
    post_messages()