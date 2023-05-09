#This python script manages the interface between python and the Google Drive API. For the propper working of this script it is necessary to
#have in the same directory as the "read_logfile.py" script the "keys.json" file that stores the credentials to communicate with the Google
#Drive API.

from __future__ import print_function

import os.path
import glob, pathlib

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

#This function returns a pandas dataframe with the read columns and rows from the google drive logfile
def download_logfile(logfilename):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    PATH = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = PATH + '/keys.json'

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1FS5J8cZY2-7es1gutmjtokkPUxlqTzx_X8gpVKxBWbQ'

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=str(logfilename) + "!A1:AD1000").execute()
    values = result.get('values', [])
    DF = pd.DataFrame(values[1:], columns=values[0])
    return DF

def download_results(sheetname):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    PATH = os.path.dirname(__file__)
    SERVICE_ACCOUNT_FILE = PATH + '/keys.json'

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1FS5J8cZY2-7es1gutmjtokkPUxlqTzx_X8gpVKxBWbQ'

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=str(sheetname) + "!A1:AD75").execute()
    values = result.get('values', [])
    DF = pd.DataFrame(values)
    return DF

def read_csv():
	path = "/Users/jcapo/Downloads/Calibration-LogFile - DUNE-HD_LogFile.csv"
	DF = pd.DataFrame(pd.read_csv(path, sep=",", header=0))
	return DF