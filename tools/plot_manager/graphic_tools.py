import matplotlib.pyplot as plt

def create_fig(rows, cols, bshx, bshy):
    fig, axis = plt.subplots(nrows=rows, ncols=cols, constrained_layout=True,
                 sharex=bshx, sharey=bshy)
    axises = []
    for i in axis:
        for j in i:
            axises.append(j)
    return fig, axises
