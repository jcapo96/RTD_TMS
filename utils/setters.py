import pathlib, sys, glob
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# rootpath = pathlib.Path(__file__).parent.parent.resolve()
rootpath = "/afs/cern.ch/user/j/jcapotor/RTDana"
sys.path.insert(1, glob.glob(str(rootpath) + "/**/data_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
import read_data, select_files, defined_functions

def set_time_window(cal):
    cal["Data"] = cal["Data"][200:800]
    return cal

