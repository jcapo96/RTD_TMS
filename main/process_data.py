import pathlib, sys, glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# rootpath = pathlib.Path(__file__).parent.parent.resolve()
rootpath = "/afs/cern.ch/user/j/jcapotor/RTDana"
sys.path.insert(1, glob.glob(str(rootpath) + "/**/data_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/utils", recursive=True)[0])
import read_data, select_files
import getters, setters

def process_data():
    selection = select_files.select_files(
        "DUNE-HD_LogFile",
        **{"CalibSetNumber":"8", "Selection":"GOOD", "Type":"Cal"}
    )
    print("Reading data ...")
    data = read_data.get_data(selection)
    print("Convert timestamp to seconds in Data -> Time information is only stored in the raw dataframe")
    data = data.apply(getters.get_time_seconds, axis=1)
    print("Setting appropriate time window...")
    data = data.apply(setters.set_time_window, axis=1)
    for ref in data["Data"][0].columns:
        if ref == "TimeStamp":
            continue
        print("Using as reference " + ref + ": " + data["S"+ref[1:]][0])
        data = data.apply(getters.get_offset, args=(ref,), axis=1)
    print("Calculating calibration constants -> keys: CalConst & CalConstErr")
    data = data.apply(getters.get_calibration_constant, axis=1)
    calib, errors = getters.get_calib(data)
    return data, calib, errors

data, calib, errors = process_data()
plt.figure()
plt.imshow(errors, origin="lower", aspect="equal")
plt.axis("tight")
plt.title("Calibration Constant Errors")
plt.colorbar()
plt.show(block=True)