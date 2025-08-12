# Bulk Email Sender

This project sends personalised bulk emails using the O365 library and Microsoft Graph【875279954019257†L140-L155】. The script reads recipient details from an Excel file and sends messages with optional attachments.

## Features

- Authenticates against Microsoft Graph with OAuth【875279954019257†L140-L155】.
- Reads recipients and message templates from Excel or CSV.
- Sends individual emails with personalised content.
- Supports attachments and tracking of delivery status.

## Prerequisites

- Python 3.8 or later.
- A registered Azure AD application with mail send permissions.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Follow the O365 library instructions to create a credentials file for OAuth【875279954019257†L140-L155】.
3. Place your recipients in `recipients.xlsx` with columns `email` and `name`.
4. Edit `main.py` to set the subject and body template.
5. Run the script:
   ```
   python main.py
   ```