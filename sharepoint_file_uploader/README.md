# SharePoint File Uploader

This project uploads files to a SharePoint document library using the O365 library【875279954019257†L148-L154】. The script scans a local folder and uploads new or updated documents.

## Features

- Authenticates with Microsoft Graph or SharePoint【875279954019257†L140-L155】.
- Navigates to a SharePoint site and library【875279954019257†L148-L154】.
- Uploads files and sets metadata like title and description.
- Maintains a log of uploaded files.

## Prerequisites

- Python 3.8 or later.
- A SharePoint site with a document library.
- Install dependencies from `requirements.txt`.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Edit `main.py` to set the site name, library name, and local folder path.
3. Run the script:
   ```
   python main.py
   ```