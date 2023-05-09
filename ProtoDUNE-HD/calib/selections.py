from __future__ import print_function

import os.path

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

def download_logfile():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    SERVICE_ACCOUNT_FILE = '/afs/cern.ch/user/j/jcapotor/RTDana/ProtoDUNE-HD/calib/keys.json'

    credentials = None
    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = '1FS5J8cZY2-7es1gutmjtokkPUxlqTzx_X8gpVKxBWbQ'

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="ProtoDUNE-HD_LogFile!A1:AD5000").execute()
    values = result.get('values', [])
    DF = pd.DataFrame(values[1:], columns=values[0])
    return DF

def select_files(**kwargs):
    log_file = download_logfile()
    for i, j in kwargs.items():
        log_file = log_file.loc[(log_file[i]==j)]
    return log_file