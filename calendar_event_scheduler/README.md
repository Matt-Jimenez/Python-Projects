# Calendar Event Scheduler

This project schedules meetings or events in Outlook calendars using the O365 library【875279954019257†L140-L155】. The script reads event details from a CSV and creates calendar events with Teams links.

## Features

- Authenticates with Microsoft Graph【875279954019257†L140-L155】.
- Reads events from a CSV file with subject, start time, end time, and attendees.
- Schedules events in the user's calendar and sends invitations.
- Handles time zone conversion automatically【875279954019257†L140-L147】.

## Prerequisites

- Python 3.8 or later.
- An Azure AD application with calendar permissions.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Create `events.csv` with columns: `subject`, `start`, `end`, `attendees` (semicolon‑separated).
3. Follow O365 authentication steps to set up credentials.
4. Run the script:
   ```
   python main.py
   ```