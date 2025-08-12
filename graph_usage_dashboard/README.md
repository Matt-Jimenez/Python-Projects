# Graph Usage Dashboard

This project gathers usage statistics from Microsoft Graph and builds a dashboard. The script counts emails, calendar events, and OneDrive files and then creates charts.

## Features

- Authenticates with Microsoft Graph via the O365 library【875279954019257†L140-L155】.
- Collects counts of resources such as emails, events, and files.
- Creates charts using matplotlib.
- Exports the dashboard to Excel or PowerPoint.

## Prerequisites

- Python 3.8 or later.
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