import pandas as pd
import glob
from datetime import datetime
import dateutil.parser

def convert_timestamp_to_seconds(x):
    #this function converts the timestamp into seconds taking as reference the uNIX standard time
    date, time = x.split("-")
    day, month, year = date.split("/")
    hour, minute, second = time.split(":")
    try:
        dt = datetime(year=int(year), month=int(month), day=int(day), hour=int(hour), minute=int(minute), second=int(second))
    except:
        second, ampm = second.split(" ")
        string = year+"-"+day+"-"+month+" "+hour+":"+minute+":"+second+ampm
        dt = dateutil.parser.parse(string)
    epoch_time = datetime(1970, 1, 1)
    delta = (dt - epoch_time)
    return delta.total_seconds()

def get_data(row):
    #this function looks for the file in the folders, read the data for each selected file, converts the time to seconds frome epoch and converts the units to mK 
    path = "/eos/user/j/jcapotor/RTDdata/Data"
    text_file = glob.glob(path + "/**/" + row["Filename"] + ".txt", recursive = True)
    path_to_file = text_file[0]
    print("Path to file -------> " + path_to_file)
    names = ["Date", "Time", "s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12", "s13", "s14"]
    data = pd.DataFrame(pd.read_csv(str(path_to_file), sep='\t', header=None, names=names))
    data["Time"] = (data["Date"] + "-" + data["Time"]).apply(convert_timestamp_to_seconds)
    del data["Date"]
    data["Time"] = (data["Time"] - data["Time"][0])/1000
    data = data.apply(lambda x: x*1000)
    data = data.loc[(data["Time"] >= 1000) & (data["Time"] <= 2000)]
    return data