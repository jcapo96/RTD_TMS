#In this script there are defined some useful functions that are used to get, set, change or do any operation on dataframes
import numpy as np
import pandas as pd

def convert_time_to_seconds(x):
    date, time = x.split("-")
    d, m, y = date.split("/")
    h, mn, s = time.split(":")
    totalseconds = int(d)*24*3600 + int(m)*30*24*3600 + int(y)*365*24*3600 + int(h)*3600 + int(mn)*60 + int(s)
    return totalseconds

def calc_offset(x, ref):
    off = x.astype("float") - x[ref].astype("float")
    av_off = np.mean(off)
    return off

def cut_time(x, time_ini, time_end):
    x = x[time_ini:time_end]
    return x

def divide_data(x, npoints):
    means = {}
    means["Av_off"], means["Err_off"], means["Time_ini"], means["Time_end"] = [],[],[],[]
    nchunks = np.round(len(x)/npoints,0)
    x = np.array_split(x, nchunks)
    cnt = 0
    for chunk in x:
        means["Av_off"].append(np.mean(chunk))
        means["Err_off"].append(np.std(chunk))
        means["Time_ini"].append(cnt*len(chunk))
        means["Time_end"].append(len(chunk)*(cnt+1))
        cnt += 1
    return means

def compute_rms_per_chunk(x, col):
    means_std = []
    print(x)
    for sensor in x.index:
        means_std.append(x[sensor]["Av_off"])
    return means_std

