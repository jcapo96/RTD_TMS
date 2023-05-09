import pathlib, sys, glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# rootpath = pathlib.Path(__file__).parent.parent.resolve()
rootpath = "/afs/cern.ch/user/j/jcapotor/RTDana"
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
import read_logfile

data = read_logfile.download_results("TGradResults")

tgrad1, tgrad2, tgrad3, tgrad4, tgrad21 = data[0:15], data[15:30], data[30:45], data[45:58], data[58:]
tgrad1.columns = tgrad1.iloc[0]
tgrad1 = tgrad1.iloc[pd.RangeIndex(len(tgrad1)).drop(0)]

tgrad2 = tgrad2.reset_index(drop=True)
tgrad2.columns = tgrad2.iloc[0]
tgrad2 = tgrad2.iloc[pd.RangeIndex(len(tgrad2)).drop(0)]

tgrad3 = tgrad3.reset_index(drop=True)
tgrad3.columns = tgrad3.iloc[0]
tgrad3 = tgrad3.iloc[pd.RangeIndex(len(tgrad3)).drop(0)]

tgrad4 = tgrad4.reset_index(drop=True)
tgrad4.columns = tgrad4.iloc[0]
tgrad4 = tgrad4.iloc[pd.RangeIndex(len(tgrad4)).drop(0)]

tgrad21 = tgrad21.reset_index(drop=True)
tgrad21.columns = tgrad21.iloc[0]
tgrad21 = tgrad21.iloc[pd.RangeIndex(len(tgrad21)).drop(0)]

results = {"tgrad1":tgrad1, "tgrad2":tgrad2, "tgrad3":tgrad3, "tgrad4":tgrad4, "tgrad21":tgrad21}

def get_calconst_ref(results, absref):
    ids = []
    for key in results.keys():
        if key == "tgrad21":
            continue
        for index, row in results[key].iterrows():
            if row["IDS"] == "44123" or row["IDS"] == "44124":
                continue
            ids.append(row["IDS"])
    heatmap_off = {}
    heatmap_err = {}
    for ref in ids:
        heatmap_off[ref] = {}
        heatmap_err[ref] = {}
        for key in results.keys():
            if key == "tgrad21":
                continue
            try:
                off_ref = float(results[key].loc[results[key]['IDS'] == ref]["OFF-"+absref].values[0])
                err_ref = float(results[key].loc[results[key]['IDS'] == ref]["ERR-"+absref].values[0])
                continue
            except:
                pass
        for sens in ids:
            for key in results.keys():
                if key == "tgrad21":
                    continue
                try:
                    off_sens = float(results[key].loc[results[key]['IDS'] == sens]["OFF-"+absref].values[0])
                    err_sens = float(results[key].loc[results[key]['IDS'] == sens]["ERR-"+absref].values[0])
                    heatmap_off[ref][sens] = off_ref - off_sens
                    heatmap_err[ref][sens] = np.sqrt(err_ref**2 + err_sens**2)
                    continue
                except:
                    pass

    heatmap_off = pd.DataFrame(heatmap_off)
    heatmap_err = pd.DataFrame(heatmap_err)

    return heatmap_off, heatmap_err, ids

def get_calconst_tree(results):
    ids = []
    for key in results.keys():
        if key == "tgrad21":
            continue
        for index, row in results[key].iterrows():
            if row["IDS"] == "44123" or row["IDS"] == "44124":
                continue
            ids.append(row["IDS"])
    heatmap_off = {}
    heatmap_err = {}
    for ref in ids:
        heatmap_off[ref] = {}
        heatmap_err[ref] = {}
        for key1 in results.keys():
            if key1 == "tgrad21":
                continue
            try:
                test = float(results[key1].loc[results[key1]['IDS'] == ref]["OFF-"+ref].values[0])
                row = results[key1].loc[results[key1]['IDS'] == ref]
                if key1 == "tgrad1":
                    int_ref = "39652"
                if key1 == "tgrad2":
                    int_ref = "39647"
                if key1 == "tgrad3":
                    int_ref = "39622"
                if key1 == "tgrad4":
                    int_ref = "39610"
                off_ref = float(row["OFF-"+int_ref].values[0])
                err_ref = float(row["ERR-"+int_ref].values[0])
                break
            except:
                pass
        for sens in ids:
            for key in results.keys():
                if key == "tgrad21":
                    continue
                try:
                    test = float(results[key].loc[results[key]['IDS'] == sens]["OFF-"+sens].values[0])
                    row = results[key].loc[results[key]['IDS'] == sens]
                    if key == "tgrad1":
                        int_ref2 = "39652"
                    if key == "tgrad2":
                        int_ref2 = "39647"
                    if key == "tgrad3":
                        int_ref2 = "39622"
                    if key == "tgrad4":
                        int_ref2 = "39610"
                    off_sens = float(row["OFF-"+int_ref2].values[0])
                    err_sens = float(row["ERR-"+int_ref2].values[0])
                    int_off = float(results["tgrad21"].loc[results["tgrad21"]['IDS'] == int_ref2]["OFF-"+int_ref].values[0])
                    int_err = float(results["tgrad21"].loc[results["tgrad21"]['IDS'] == int_ref2]["ERR-"+int_ref].values[0])
                    heatmap_off[ref][sens] = off_ref - int_off - off_sens
                    heatmap_err[ref][sens] = np.sqrt(err_ref**2 + int_err**2 + err_sens**2)
                    break
                except:
                    pass
    
    heatmap_off = pd.DataFrame(heatmap_off)
    heatmap_err = pd.DataFrame(heatmap_err)
    return heatmap_off, heatmap_err, ids


tree_off, tree_err, ids = get_calconst_tree(results)
ref_off, ref_err, ids = get_calconst_ref(results, "44123")
ref2_off, ref2_err, ids = get_calconst_ref(results, "44124")

plt.figure()
plt.hist(tree_off["39655"].values, color="blue", label="TREE method")
plt.xlabel("Calibration Constant (mK)", fontsize=12)
plt.ylabel("Counts", fontsize=12)
plt.title("Calibration Constant wrt ID: 39655", fontsize=18)
plt.grid("On")
plt.legend()
plt.figure()
plt.hist(ref_off["39655"].values, color="orange", label="REFERENCES method")
plt.xlabel("Calibration Constant (mK)", fontsize=12)
plt.ylabel("Counts", fontsize=12)
plt.title("Calibration Constant wrt ID: 39655", fontsize=18)
plt.grid("On")
plt.legend()
plt.figure()
plt.hist(tree_err["39655"].values, color="blue", label="TREE method")
plt.xlabel("Cal. Const. Error (mK)", fontsize=12)
plt.ylabel("Counts", fontsize=12)
plt.title("Calibration Constant Errors wrt ID: 39655", fontsize=18)
plt.grid("On")
plt.legend()
plt.figure()
plt.hist(ref_err["39655"].values, color="orange", label="REFERENCES method")
plt.xlabel("Cal. Const. Error (mK)", fontsize=12)
plt.ylabel("Counts", fontsize=12)
plt.title("Calibration Constant Errors wrt ID: 39655", fontsize=18)
plt.grid("On")
plt.legend()
plt.show(block=True)


# plt.figure(constrained_layout=True)
# plt.imshow(tree_off, cmap="RdYlBu")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Values (mK) \nOffsets calculated through tree method")
# plt.xlabel("Sensor ID")
# plt.ylabel("Sensor ID")
# plt.colorbar()
# plt.figure()
# plt.hist(tree_err[0:1].values)
# plt.title("Calibration Constant Errors (mK) \nwrt ID:39655")
# plt.xlabel("Calibration Constant Errors (mK)")
# plt.ylabel("Counts")
# plt.subplot(1,3,2)
# plt.imshow(ref_off, cmap="RdYlBu")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Values (mK) \nOffsets calculated through reference 44123")
# plt.xlabel("Sensor ID")
# plt.ylabel("Sensor ID")
# plt.subplot(1,3,3)
# plt.imshow(ref2_off, cmap="RdYlBu")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Values (mK) \nOffsets calculated through reference 44124")
# plt.xlabel("Sensor ID")
# plt.ylabel("Sensor ID")
# plt.colorbar()

# plt.figure(constrained_layout=True)
# plt.imshow(tree_err, cmap="inferno")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Errors (mK) \nErrors calculated through tree")
# plt.colorbar()
# plt.subplot(1,3,2)
# plt.imshow(ref_err, cmap="inferno")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Errors (mK) \nErrors calculated through reference 44123")
# plt.colorbar()
# plt.subplot(1,3,3)
# plt.imshow(ref2_err, cmap="inferno")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Errors (mK) \nErrors calculated through reference 44124")
# plt.colorbar()

# plt.figure(constrained_layout=True)
# plt.imshow(tree_off - ref_off, cmap="RdYlBu")
# plt.axis("tight")
# plt.xticks(range(len(ids)), ids, rotation=90)
# plt.yticks(range(len(ids)), ids)
# plt.title("Calibration Constant Values (mK) \nDifference between tree and ref44123")
# plt.colorbar()

# plt.figure()
# plt.hist(tree_off["39655"][0:12] - ref_off["39655"][0:12])
# plt.xlabel("Calibration Constant Difference wrt 39655 (mK)")
# plt.title("Comparison of both methods") 