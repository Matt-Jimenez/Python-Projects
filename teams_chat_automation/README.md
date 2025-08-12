# Teams Chat Automation

This script posts messages to Microsoft Teams channels or group chats using Microsoft Graph. The script reads messages from a text file and posts them on a schedule.

## Features

- Authenticates with Microsoft Graph via the O365 library【875279954019257†L140-L155】.
- Posts messages to specified Teams channels.
- Supports group chats for project teams.
- Schedules messages at defined intervals.

## Prerequisites

- Python 3.8 or later.
- A Teams tenant and Azure AD application with chat permissions.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set your Azure AD credentials in `main.py`.
3. Edit `messages.txt` with the channel ID and message content.
4. Run the script:
   ```
   python main.py
   ```