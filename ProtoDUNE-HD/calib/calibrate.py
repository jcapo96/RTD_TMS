from __future__ import print_function

import os.path

import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.oauth2 import service_account

import pandas as pd
import numpy as np
import selections, utils, control_plots

pd.options.mode.chained_assignment = None  # default='warn'

def get_cc(selection):
    cc = {}
    cnt = 1
    n_files =len(selection)
    for index, row in selection.iterrows():
        data = utils.get_data(row)
        for ref in data.columns:
            if ref == "Time" or row["S"+ref.split("s")[1]] == "9999":
                continue
            if cnt == 1:
                cc[row["S"+ref.split("s")[1]]] = {}
                cc[row["S"+ref.split("s")[1]]+"_err"] = {}
                cc[row["S"+ref.split("s")[1]]+"_sist"] = {}
            for sens in data.columns:
                if sens == "Time" or row["S"+sens.split("s")[1]] == "9999":
                    continue
                off = data[ref] - data[sens]
                if cnt == 1:
                    cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]] = [np.mean(off)]
                    cc[row["S"+ref.split("s")[1]]+"_sist"][row["S"+sens.split("s")[1]]] = [np.std(off)]
                else:
                    if cnt == n_files:
                        cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]].append(np.mean(off))
                        cc[row["S"+ref.split("s")[1]]+"_sist"][row["S"+sens.split("s")[1]]].append(np.std(off))
                        cc = pd.DataFrame(cc)
                        cc[row["S"+ref.split("s")[1]]+"_sist"][row["S"+sens.split("s")[1]]] = np.mean(cc[row["S"+ref.split("s")[1]]+"_sist"][row["S"+sens.split("s")[1]]])
                        cc[row["S"+ref.split("s")[1]]+"_err"][row["S"+sens.split("s")[1]]] = np.std(cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]])
                        cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]] = np.mean(cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]])
                    else:
                        cc[row["S"+ref.split("s")[1]]][row["S"+sens.split("s")[1]]].append(np.mean(off))
                        cc[row["S"+ref.split("s")[1]]+"_sist"][row["S"+sens.split("s")[1]]].append(np.std(off))
        cnt += 1
    return cc

def upload_rescal(calibration, cell):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        SERVICE_ACCOUNT_FILE = '/afs/cern.ch/user/j/jcapotor/RTDana/ProtoDUNE-HD/calib/keys.json'

        credentials = None
        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # The ID and range of a sample spreadsheet.
        SAMPLE_SPREADSHEET_ID = '1FS5J8cZY2-7es1gutmjtokkPUxlqTzx_X8gpVKxBWbQ'

        calibration = calibration.values.tolist()
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range="Sheet11!B"+str(cell), valueInputOption="RAW", body={"values":calibration}).execute()

        # # Call the Sheets API
        # sheet = service.spreadsheets()

def make_calib():
    calsets = [
        {"CalibSetNumber":"TGrad-1","Selection":"FIRST_RUN", "Type":"Cal"},
        {"CalibSetNumber":"TGrad-2","Selection":"FIRST_RUN", "Type":"Cal"},
        {"CalibSetNumber":"TGrad-3","Selection":"FIRST_RUN", "Type":"Cal"},
        {"CalibSetNumber":"TGrad-4","Selection":"FIRST_RUN", "Type":"Cal"},
        {"CalibSetNumber":"TGrad-2.1","Selection":"GOOD", "Type":"Cal"},
        # {"CalibSetNumber":"Pipe-1", "Type":"Cal"},
        # {"CalibSetNumber":"Pipe-TGrad-1", "Type":"Cal"},
        # {"CalibSetNumber":"Pipe-2", "Type":"Cal"},
        # {"CalibSetNumber":"GA-PM-PP-1", "Type":"Cal"},
        # {"CalibSetNumber":"GA-PM-PP-2", "Type":"Cal"},
        # {"CalibSetNumber":"GA-STD-1", "Type":"Cal"},
        # {"CalibSetNumber":"GA-STD-2", "Type":"Cal"},
        # {"CalibSetNumber":"GA-STD-HP", "Type":"Cal"},
    ]
    cell = 1
    for calset in calsets:
        selection = selections.select_files(**calset)
        cc = get_cc(selection)
        cc["ID"] = cc.index
        cc["Calset"] = [calset["CalibSetNumber"]]*len(cc)
        cc = cc.columns.to_frame().T.append(cc, ignore_index=True)
        cc.columns = range(len(cc.columns))
        print(cc)
        upload_rescal(cc, cell)
        cell = cell + len(cc)

make_calib()
