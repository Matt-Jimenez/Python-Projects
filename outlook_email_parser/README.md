# Outlook Email Parser

This project scans an Outlook mailbox, filters messages, and downloads attachments using the O365 library【875279954019257†L150-L153】. The script stores attachments locally and logs message metadata.

## Features

- Authenticates with Microsoft Graph via O365【875279954019257†L140-L155】.
- Filters messages by subject, sender, or date.
- Downloads attachments and saves them to disk.
- Logs details like subject, sender, and received time.

## Prerequisites

- Python 3.8 or later.
- An Outlook mailbox accessible via Microsoft Graph.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Set your Azure AD credentials in `main.py`.
3. Run the script:
   ```
   python main.py
   ```