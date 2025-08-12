"""
SharePoint file uploader.

Uploads files from a local folder to a SharePoint document library using the O365 library.
"""

import os
from O365 import Account

# Replace with your Azure AD app credentials and SharePoint details
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
SITE_NAME = 'MySite'
LOCAL_FOLDER = 'upload'


def authenticate():
    credentials = (CLIENT_ID, CLIENT_SECRET)
    account = Account(credentials)
    if not account.is_authenticated:
        account.authenticate(scopes=['https://graph.microsoft.com/Sites.ReadWrite.All'])
    return account


def upload_files():
    """Upload files from LOCAL_FOLDER to the default document library."""
    account = authenticate()
    sharepoint = account.sharepoint()
    site = sharepoint.get_site(site_name=SITE_NAME)
    drive = site.get_default_document_library()
    for filename in os.listdir(LOCAL_FOLDER):
        filepath = os.path.join(LOCAL_FOLDER, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'rb') as file_obj:
                drive.upload_file(file_obj, filename)
                print(f'Uploaded {filename}')


if __name__ == '__main__':
    upload_files()