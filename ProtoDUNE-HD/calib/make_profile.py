import pandas as pd
import numpy as np
import selections, utils, control_plots

import matplotlib.pyplot as plt
import make_tree

path_to_cal = "/eos/user/j/jcapotor/RTDdata/Data/TGrad_Calibs/migue_cal.txt"
path_to_data = "/eos/user/j/jcapotor/RTDdata/Data/TGrad_Calibs/TP_normal.txt"

cal = pd.read_csv(path_to_cal, header=0)
data = pd.read_csv(path_to_data, header=0)
cal.index = cal["sensor"]
del cal["sensor"]

new_cal = pd.Series(make_tree.make_tree()).rename("calib").to_frame()

for index, row in cal.iterrows():
    cal["offset"][index] = (cal["offset"][index] - cal["offset"][39652])*1000
    cal["offset45"][index] = new_cal["calib"][str(index)] - new_cal["calib"]["39652"]

cal.index = cal["height"]
data.index = data["perfil"]

data = data[data["normal"] > 50]

corr_migue = []
corr_jordi = []
for index, row in data.iterrows():
    corr_migue.append(data["normal"][index]*1000 - cal["offset"][index])
    corr_jordi.append(data["normal"][index]*1000 - cal["offset45"][index])
