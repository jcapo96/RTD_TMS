import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import selections, utils

def create_figure(nrows, ncols):
    #this function just creates the figure with axes in such a way it is easy to iterate over
    fig, axes = plt.subplots(nrows = nrows, ncols = ncols, constrained_layout=True)
    axis = []
    for i in axes:
        for j in i:
            axis.append(j)
    return fig, axis

def plot_temperatures(selection):
    fig, axes = create_figure(3,5)
    fig.suptitle("Temperature (mK) vs Time (s) \nTemperature evolution")
    for index, row in selection.iterrows():
        data = utils.get_data(row)
        for col in data.columns:
            if col == "Time":
                continue
            cnt = int(col.split("s")[1])-1
            temp = data[col] - data[col].values[0]
            time = data["Time"] - data["Time"].values[0]
            axes[cnt].plot(time, temp, "o", alpha=0.5, label=row["N_Run"])
            axes[cnt].axhline(y=np.mean(temp), color="black", linestyle="-", linewidth=4.5)
            axes[cnt].set_title("ID:" + row["S"+str(cnt+1)])

def plot_offsets(selection, ref, color):
    fig, axes = create_figure(3,5)
    fig.suptitle("Offset (mK) vs Time (s) \nReference: " + selection["S"+ref.split("s")[1]].any())

    n_files = len(selection)
    offsets = np.zeros((14, n_files))
    offsets_errors = np.zeros((14, n_files))
    for index, row in selection.reset_index(drop=True).iterrows():
        data = utils.get_data(row)
        for col in data.columns:
            if col == "Time":
                continue
            cnt = int(col.split("s")[1])-1
            off = data[col] - data[ref]
            time = data["Time"]
            axes[cnt].plot(time, off, "o", alpha=0.5, label=row["N_Run"])
            axes[cnt].axhline(y=np.mean(off), color="black", linestyle="-", linewidth=4.5)
            axes[cnt].set_title("ID:" + row["S"+str(cnt+1)])

            offsets[cnt][index] = np.mean(off)
            offsets_errors[cnt][index] = np.std(off)
    
    cc = np.mean(offsets, axis=1)
    #to correctly propagate these errors it is needed to look for the appropriate formula, I don't know if it is correct to divide by the number of measurements
    cc_err = np.sqrt((np.std(offsets, axis=1)**2 + np.sqrt(np.sum(offsets_errors**2, axis=1)/len(offsets_errors))**2))
    axes[-1].scatter(range(len(cc_err)), cc_err)
    axes[-1].set_xticks(range(len(cc_err)))
    axes[-1].set_xticklabels(labels=data.columns[1:], rotation=90)
    axes[-1].set_title("CC errors (mK)")
    return fig, axes

# selection2 = selections.select_files(**{"CalibSetNumber":"TGrad-2.1", "Selection":"GOOD", "Type":"Cal"})
# plot_offsets(selection2, "s1", color="red")
# plt.show(block=True)