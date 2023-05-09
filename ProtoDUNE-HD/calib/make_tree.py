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
import ref_vs_bath

pd.options.mode.chained_assignment = None  # default='warn'

def download_calibration():
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
                                range="ProtoDUNE-HD_Results!A1:AR5000").execute()
    values = result.get('values', [])
    DF = pd.DataFrame(values)
    return DF

def divide_data_in_sets():
    data = download_calibration()
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


def make_tree():
    sets = divide_data_in_sets()
    offsets = {}
    tree_ref = "39652"
    tgrad1_ref = "39652"
    for calset in sets:
        if calset == "TGrad-2.1":
            continue
        for index, row in sets[calset].iterrows():
            if index == "44123" or index == "44124":
                continue
            if calset == "TGrad-1":
                offsets[index] = -sets[calset][tree_ref][index]
            if calset == "TGrad-2":
                tgrad2_ref = "39647"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref])
            if calset == "TGrad-3":
                tgrad2_ref = "40533"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref])
            if calset == "TGrad-4":
                tgrad2_ref = "39661"
                offsets[index] = -(sets[calset][tgrad2_ref][index] + sets["TGrad-2.1"][tgrad1_ref][tgrad2_ref] + sets["TGrad-1"][tree_ref][tgrad1_ref])
    return offsets

def make_ref():
    sets = divide_data_in_sets()
    results = np.linspace(0,4,1)
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
                offsets[index] = sets[calset][ref][index] - results[0]
            if calset == "TGrad-2":
                tgrad2_ref = "39647"
                offsets[index] = sets[calset][ref][index] - results[1]
            if calset == "TGrad-3":
                tgrad2_ref = "40533"
                offsets[index] = sets[calset][ref][index] - results[2]
            if calset == "TGrad-4":
                tgrad2_ref = "39661"
                offsets[index] = sets[calset][ref][index] - results[3]
    return offsets

# offsets_tree = make_tree()
# offsets_ref = make_ref()

# results = []
# for key in offsets_tree:
#     results.append(np.round(offsets_ref[key] + offsets_tree[key], 1))


# diff1 = calculate_comparison(ref1, tree_ref)
# diff2 = calculate_comparison(ref2, tree_ref)

# diff3 = calculate_comparison(ref1, "39657")
# diff4 = calculate_comparison(ref2, "39657")

################################################################################################################################################################################################################

# off = {}
# ref_calset = "TGrad-1"
# tgrad1 = ["39655","39654","39653","39652","39651","39650","40526","40525","40524","39659","39658","39657"]
# primary_refs = ["39652", "40525", "39657"]
# sec_refs_tg1 = primary_refs
# sec_refs_tg2 = ["39647", "39629", "39625"]
# sec_refs_tg3 = ["39622", "40533", "39613"]
# sec_refs_tg4 = ["39610", "39666", "39661"]
# for ref in tgrad1[3:4]:
#     print(ref)
#     for primary_ref in primary_refs:
#         for sec_ref_tg1 in sec_refs_tg1:
#             for sec_ref_tg2 in sec_refs_tg2:
#                 for sec_ref_tg3 in sec_refs_tg3:
#                     for sec_ref_tg4 in sec_refs_tg4:
#                         off[ref+primary_ref+sec_ref_tg1+sec_ref_tg2+sec_ref_tg3+sec_ref_tg4] = {}
#                         # off[ref+primary_ref+sec_ref_tg2+"_err"] = {}
#                         for calset in sets.keys():
#                             if calset == "TGrad-1":
#                                 sec_ref = sec_ref_tg1
#                                 for index, row in sets[calset].iterrows():
#                                     if index == "44123" or index == "44124":
#                                         continue
#                                     off[ref+primary_ref+sec_ref_tg1+sec_ref_tg2+sec_ref_tg3+sec_ref_tg4][index+"_TG1"] = row[sec_ref] + sets["TGrad-2.1"][primary_ref][sec_ref] + sets[ref_calset][ref][primary_ref]
#                                     # off[ref+primary_ref+sec_ref_tg2+"_err"][index+"_TG1"] = row[ref+"_err"]
#                             # if calset == "TGrad-2":
#                             #     sec_ref = sec_ref_tg2
#                             #     for index, row in sets[calset].iterrows():
#                             #         if index == "44123" or index == "44124":
#                             #             continue
#                             #         off[ref+primary_ref+sec_ref_tg1+sec_ref_tg2+sec_ref_tg3+sec_ref_tg4][index+"_TG2"] = row[sec_ref] + sets["TGrad-2.1"][primary_ref][sec_ref] + sets[ref_calset][ref][primary_ref]
#                             #         # off[ref+primary_ref+sec_ref_tg2+"_err"][index+"_TG2"] = np.sqrt(row[sec_ref+"_err"]**2 + sets["TGrad-2.1"][primary_ref+"_err"][sec_ref]**2 + sets[ref_calset][ref+"_err"][primary_ref]**2)
#                             # if calset == "TGrad-3":
#                             #     sec_ref = sec_ref_tg3
#                             #     for index, row in sets[calset].iterrows():
#                             #         if index == "44123" or index == "44124":
#                             #             continue
#                             #         off[ref+primary_ref+sec_ref_tg1+sec_ref_tg2+sec_ref_tg3+sec_ref_tg4][index+"_TG3"] = row[sec_ref] + sets["TGrad-2.1"][primary_ref][sec_ref] + sets[ref_calset][ref][primary_ref]
#                             # # off[ref+primary_ref+sec_ref_tg2+"_err"][index+"_TG3"] = np.sqrt(row[sec_ref+"_err"]**2 + sets["TGrad-2.1"][primary_ref+"_err"][sec_ref]**2 + sets[ref_calset][ref+"_err"][primary_ref]**2)
#                             # if calset == "TGrad-4":
#                             #     sec_ref = sec_ref_tg4
#                             #     for index, row in sets[calset].iterrows():
#                             #         if index == "44123" or index == "44124":
#                             #             continue
#                             #         off[ref+primary_ref+sec_ref_tg1+sec_ref_tg2+sec_ref_tg3+sec_ref_tg4][index+"_TG4"] = float(row[sec_ref]) + float(sets["TGrad-2.1"][primary_ref][sec_ref]) + float(sets[ref_calset][ref][primary_ref])
#                             #     #off[ref+primary_ref+"_err"][index+"_TG4"] = np.sqrt(float(row[sec_ref+"_err"])**2 + float(sets["TGrad-2.1"][primary_ref+"_err"][sec_ref])**2 + float(sets[ref_calset][ref+"_err"][primary_ref])**2)


# off = pd.DataFrame(off)
# results = []
# cnt = 0
# for col in off.columns:
#     for refcol in off.columns:
#         for index, row in off.iterrows():
#             cc_diff = (row[col]-row[refcol])
#             if np.abs(cc_diff) > 5:
#                 continue
#             results.append(cc_diff)
#         cnt += 1

# plt.hist(results)
# print(len(results))
# print(np.mean(results))
# print(np.std(results))
# plt.show(block=True)