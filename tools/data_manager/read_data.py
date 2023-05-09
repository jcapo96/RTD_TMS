import pathlib, sys, glob
import pandas as pd
import numpy as np

# rootpath = pathlib.Path(__file__).parent.parent.resolve()
rootpath = "/afs/cern.ch/user/j/jcapotor/RTDana"
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
import select_files

def find_data(row):
    data_path = glob.glob("/eos/user/j/jcapotor" + "/**/" + str(row["Filename"]) + ".txt",
                          recursive=True)[0]
    data = pd.DataFrame(pd.read_csv(data_path, sep="\t",
                                    header=None,
                                    names=select_files.create_header(row)))
    data['TimeStamp'] = data[['Date', 'Time']].agg('-'.join, axis=1)
    del data["Time"], data["Date"]
    return data

def get_data(selection):
    selection["Data"] = selection.apply(find_data, axis=1)
    return selection
