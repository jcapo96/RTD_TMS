import pathlib, sys, glob
import numpy as np
import matplotlib.pyplot as plt

rootpath = pathlib.Path(__file__).parent.parent.parent.resolve()
sys.path.insert(1, glob.glob(str(rootpath) + "/**/data_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/file_manager", recursive=True)[0])
sys.path.insert(1, glob.glob(str(rootpath) + "/**/plot_manager", recursive=True)[0])
import read_data, select_files, graphic_tools, add_data

def plot_temp(selection):
    df = read_data.get_data(selection)
    fig, axes = graphic_tools.create_fig(2, 7, True, True)
    fig.suptitle("Temperature vs Time \nCalibSetNumber: " + str(df["CalibSetNumber"].unique()),
        fontweight="bold")
    for index, row in df.iterrows():
        for chan in range(1,15):
            axes[chan-1].plot(row["Data"]["Time"], row["Data"]["s"+str(chan)])
            if chan <= 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, fontweight="bold")
            if chan > 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, y = -0.1, fontweight="bold")
                axes[chan-1].xaxis.tick_top()
            axes[chan-1].grid("on")
            if chan == 1 or chan == 8: 
                axes[chan-1].set_ylabel("Temperature (K)", 
                    fontweight="bold")
    fig.subplots_adjust(hspace=.0)
    fig.subplots_adjust(wspace=.0)
    return fig, axes

def plot_scatter(selection):
    df = read_data.get_data(selection)
    fig, axes = graphic_tools.create_fig(2, 7, True, True)
    for index, row in df.iterrows():
        for chan in range(1,15):
            for ref in range(1,15):
                axes[chan-1].plot(row["Data"]["s"+str(chan)] - row["Data"]["s"+str(chan)][0], row["Data"]["s"+str(ref)]- row["Data"]["s"+str(ref)][0],
                ".", color="black")
            if chan <= 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, fontweight="bold")
            if chan > 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, y = -0.1, fontweight="bold")
                axes[chan-1].xaxis.tick_top()
            axes[chan-1].grid("on")
            if chan == 1 or chan == 8: 
                axes[chan-1].set_ylabel("Temperature (K)", 
                    fontweight="bold")
    fig.subplots_adjust(hspace=.0)
    fig.subplots_adjust(wspace=.0)
    fig.suptitle("CalibSetNumber: " + str(df["CalibSetNumber"].unique()),
        fontweight="bold")
    return fig, axes

def plot_off(selection, ref):
    df = read_data.get_data(selection)
    fig, axes = graphic_tools.create_fig(2, 7, True, True)
    fig.suptitle("Temperature vs Time \nCalibSetNumber: " + str(df["CalibSetNumber"].unique()),
        fontweight="bold")
    for index, row in df.iterrows():
        for chan in range(1,15):
            axes[chan-1].plot(row["Data"]["Time"], row["Data"]["s"+str(chan)] - row["Data"][ref] - np.mean(df["Data"][0]["s"+str(chan)] - df["Data"][0][ref]))
            if chan <= 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, fontweight="bold")
            if chan > 7:
                axes[chan-1].set_title("s" + str(chan) + " ID: " + row["S"+str(chan)],
                        fontsize=10, y = -0.1, fontweight="bold")
                axes[chan-1].xaxis.tick_top()
            axes[chan-1].grid("on")
            if chan == 1 or chan == 8: 
                axes[chan-1].set_ylabel("Temperature (K)", 
                    fontweight="bold")
    fig.subplots_adjust(hspace=.0)
    fig.subplots_adjust(wspace=.0)
    return fig, axes

def plot_linear_regression(selection):
    df = read_data.get_data(selection)
    df = add_data.add_linear_regression(df)
    fig, axes = graphic_tools.create_fig(3,3, False, False)
    fig.suptitle("Regression Fit Distributions \nCalibSetNumber: " + str(df["CalibSetNumber"].unique()),
        fontweight="bold")
    y0s, slopes, slopes_err, r2s = [], [], [], []
    for index, row in df.iterrows():
        y0s += (row["LinRegr"]["y0"])
        slopes += (row["LinRegr"]["slope"])
        slopes_err += (row["LinRegr"]["slope_err"])
        r2s += (row["LinRegr"]["r2"])
    axes[0].hist(y0s, bins=20, label= "Mean: " + str(np.round(np.mean(y0s), 3)) + "\n+- " + str(np.round(np.std(y0s), 3)))
    axes[0].set_title("Interception values Distribution")
    axes[0].set_xlabel("Intercept (AU)")
    axes[0].legend()
    axes[1].hist(slopes, bins=20, label= "Mean: " + str(np.round(np.mean(slopes), 3)) + "\n+- " + str(np.round(np.std(slopes), 3)))
    axes[1].set_title("Slopes values Distribution")
    axes[1].set_xlabel("Slope (ad.)")
    axes[1].legend()
    axes[2].hist(slopes_err, bins=20, label= "Mean: " + str(np.round(np.mean(slopes_err), 3)) + "\n+- " + str(np.round(np.std(slopes_err), 3)))
    axes[2].set_title("Slope Errors values Distribution")
    axes[2].set_xlabel("Slope error (ad.)")
    axes[2].legend()
    axes[3].hist(r2s, bins=20, label= "Mean: " + str(np.round(np.mean(r2s), 3)) + "\n+- " + str(np.round(np.std(r2s), 3)))
    axes[3].set_title("R2 values Distribution")
    axes[3].set_xlabel("R2 (ad.)")
    axes[3].legend()
    axes[4].scatter(slopes, slopes_err)
    axes[4].set_title("Slope vs Slope Error")
    axes[4].set_xlabel("Slope")
    axes[4].set_ylabel("Slope Error")
    axes[4].legend()
    axes[5].scatter(slopes, r2s)
    axes[5].set_title("Slope vs R2")
    axes[5].set_xlabel("Slope")
    axes[5].set_ylabel("R2")
    axes[5].legend()
    axes[6].scatter(slopes, y0s)
    axes[6].set_title("Slope vs Interception")
    axes[6].set_xlabel("Slope")
    axes[6].set_ylabel("Interception")
    axes[6].legend()
    axes[7].scatter(y0s, r2s)
    axes[7].set_title("Interception vs R2")
    axes[7].set_xlabel("Interception")
    axes[7].set_ylabel("R2")
    axes[7].legend()
    axes[8].scatter(slopes_err, r2s)
    axes[8].set_title("Slopes Error vs R2")
    axes[8].set_xlabel("Slopes Error")
    axes[8].set_ylabel("R2")
    axes[8].legend()
    return fig, axes

selection = select_files.select_files("DUNE-HD_LogFile", **{"CalibSetNumber":"8", "Selection":"GOOD", "Type":"Cal"})
plot_linear_regression(selection)
plt.show(block=True)
