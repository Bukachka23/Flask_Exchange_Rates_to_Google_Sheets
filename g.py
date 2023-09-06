import pickle
import os
import datetime

from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

# Function to create a Google API service client
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    # Print the function arguments for debugging
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    # Set variables based on function arguments
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    # Convert scopes tuple to list
    SCOPES = [scope for scope in scopes[0]]
    # Print the scopes for debugging
    print(SCOPES)

    # Initialize credentials variable
    cred = None

    # Generate a filename for the pickle file to store tokens
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    # Check if pickle file exists
    if os.path.exists(pickle_file):
        # Load credentials from pickle file
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    # Check if credentials are valid
    if not cred or not cred.valid:
        # Refresh credentials if expired
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            # Create new credentials
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        # Save the credentials to a pickle file
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        # Build and return the Google API service client
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        # Print success message
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        # Print error message and return None if service creation fails
        print('Unable to connect.')
        print(e)
        return None

# Function to convert a datetime to RFC format
def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    # Create a datetime object and convert it to ISO format with a 'Z' appended
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
