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

import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'

def download_calibration(sheetname):
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
                                range=sheetname+"!A1:AR5000").execute()
    values = result.get('values', [])
    DF = pd.DataFrame(values)
    return DF

def divide_data_in_sets(sheetname):
    data = download_calibration(sheetname)
    sets = {}
    for i in [0,15,30,45,60]:
        set = data[i:15+i].reset_index(drop=True)
        set.columns = set.iloc[0]
        set.index = set["ID"]
        set = set.drop("ID")
        del set["ID"]
        calset = set["Calset"][5]
        del set["Calset"]
        sets[calset] = set.astype(float)
    return sets

def get_correction_tree(tgrad1_ref, tgrad2_ref, tgrad3_ref, tgrad4_ref):
    sheetname = "ProtoDUNE-HD_Results"
    results = []
    sets = divide_data_in_sets(sheetname)
    offsets = {}
    tree_ref = "39652"
    tgrad1_ref = "39652"
    ref = "44123"
    for calset in sets:
        if calset == "TGrad-2.1":
            continue
        for index, row in sets[calset].iterrows():
            if index == "44123" or index == "44124":
                continue
            if calset == "TGrad-1":
                if index != "39652":
                    continue
                offsets[index] = -sets[calset][tree_ref][index] + sets["TGrad-1"][ref][index]
                results.append(-sets[calset][tree_ref][index] + sets["TGrad-1"][ref][index])
            if calset == "TGrad-2":
                if index != "39649":
                    continue
                tgrad2_ref = "39647"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-2"][ref][index]
                results.append(-(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-2"][ref][index])
            if calset == "TGrad-3":
                if index != "40533":
                    continue
                tgrad2_ref = "40533"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-3"][ref][index]
                results.append(-(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-3"][ref][index])
            if calset == "TGrad-4":
                if index != "39661":
                    continue
                tgrad2_ref = "39661"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-4"][ref][index]
                results.append(-(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref]) + sets["TGrad-4"][ref][index])
    return results

def get_correction():
    sheetnames = ["ProtoDUNE-HD_Results_1","ProtoDUNE-HD_Results"]
    offsets = {}
    baths = {}
    raised = ["39652", "40525", "39657", "39647", "39629", "39625", "39622", "40533", "39613", "39610", "39666", "39610"]
    absref = "44123"
    for ref in raised:
        offsets[ref] = []
        baths[ref] = []
    for sheetname in sheetnames:
        sets = divide_data_in_sets(sheetname)
        for ref in raised:
            for calset in sets.keys():
                if calset == "TGrad-2.1":
                    continue
                if ref in sets[calset].index:
                    offsets[ref].append(-sets[calset][ref][absref])
                    offsets[ref].append(-sets["TGrad-2.1"][ref][absref])
                    if calset == "TGrad-1" and sheetname == "ProtoDUNE-HD_Results_1":
                        baths[ref].append(2)
                        baths[ref].append(31)
                    if calset == "TGrad-2" and sheetname == "ProtoDUNE-HD_Results_1":
                        baths[ref].append(6)
                        baths[ref].append(31)
                    if calset == "TGrad-3" and sheetname == "ProtoDUNE-HD_Results_1":
                        baths[ref].append(10)
                        baths[ref].append(31)
                    if calset == "TGrad-4" and sheetname == "ProtoDUNE-HD_Results_1":
                        baths[ref].append(19)
                        baths[ref].append(31)
                    if calset == "TGrad-1" and sheetname == "ProtoDUNE-HD_Results":
                        baths[ref].append(48)
                        baths[ref].append(31)
                    if calset == "TGrad-2" and sheetname == "ProtoDUNE-HD_Results":
                        baths[ref].append(52)
                        baths[ref].append(31)
                    if calset == "TGrad-3" and sheetname == "ProtoDUNE-HD_Results":
                        baths[ref].append(56)
                        baths[ref].append(31)
                    if calset == "TGrad-4" and sheetname == "ProtoDUNE-HD_Results":
                        baths[ref].append(60)
                        baths[ref].append(31)

    return offsets, baths

offsets, baths = get_correction()

# for key in offsets.keys():
#     plt.plot(baths[key], offsets[key] - offsets[key][0], label=str(key)+"-44123")
# plt.title("Offset 44123 - raised sensors")
# plt.xlabel("Number of baths")
# plt.ylabel("Offset wrt 44123")
# plt.legend()
# plt.show(block=True)
# x = [48, 52, 56, 60]
# xerr = [2, 2, 2, 2]
# yerr = [3, 3, 3, 3]
# plt.figure()
# plt.errorbar(x, results-results[0], xerr=xerr, yerr=yerr, fmt="o")
# plt.xlabel("Number of baths")
# plt.ylabel("Offset 39652-44123")
# plt.title("Reference vs number of baths")
# plt.show(block=True)
