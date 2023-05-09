import pathlib, sys, glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# rootpath = pathlib.Path(__file__).parent.parent.resolve()
rootpath = "/afs/cern.ch/user/j/jcapotor/RTDana"
sys.path.insert(1, glob.glob(str(rootpath) + "/**/data_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
import read_data, select_files, defined_functions

def get_time_seconds(cal):
    cal["Data"]["TimeStamp"] = cal["Data"]["TimeStamp"].apply(defined_functions.convert_time_to_seconds)
    return cal

def get_offset(cal, ref):
    print("Processing Run: " + cal["N_Run"])
    cal["Off_R"+ref] = (
    cal["Data"].select_dtypes(exclude="object")
    .apply(defined_functions.calc_offset, args=(ref,), axis=1)
    .join(cal["Data"].select_dtypes(include=("object")))
    .loc[:, cal["Data"].columns.to_list()]
    )
    del cal["Off_R"+ref]["TimeStamp"]
    return cal

def get_calibration_constant(cal):
    av_offsets, err_offsets = {}, {}
    for ref in cal["Data"].columns:
        if ref == "TimeStamp":
            continue
        else:
            av_offsets["CC_"+ref] = (cal["Off_R"+ref]
                .apply(lambda x: np.mean(x))
            )
            err_offsets["CC_Err_"+ref] = (cal["Off_R"+ref]
                .apply(lambda x: np.std(x))
            )
    cal["CalConst"] = pd.DataFrame(av_offsets)
    cal["CalConstErr"] = pd.DataFrame(err_offsets)
    return cal

def get_calib(cal):
    df_average = cal["CalConst"][0].copy()
    df_error = []
    for index, row in cal.iterrows():
        if index == 0:
            continue
        df_average += cal["CalConst"][index].copy()
        df_error.append(cal["CalConst"][index].copy())
    return df_average/len(cal), pd.DataFrame(np.std(df_error, axis=0))

def get_rms_per_sensor_per_chunk(cal, col, npoints):
    cal["RMS_per_sensor_per_chunk_"+col] = (
        cal[col]
        .apply(defined_functions.divide_data, args=(npoints,), axis=0)
    )
    return cal

def get_rms_per_chunk(cal, col):
    cal["RMS_per_chunk"+col] = (
        cal["RMS_per_sensor_per_chunk_"+col]
        .apply(defined_functions.compute_rms_per_chunk, args=(col,))
    )


# for i in range(1,15):
#     print("Reference is: s" + str(i))
#     data = data.apply(get_offset, args=("s"+str(i),), axis=1)
# data = data.apply(get_time_seconds, axis=1)
# data = data.apply(get_calibration_constant, axis=1)
# print(data["CalConst"][0])