import read_logfile

def select_files(logfilename, **kwargs):
    #the selection is made by giving kwargs to that function as a dictionary
    log_file = read_logfile.download_logfile(logfilename)
    selection = log_file.copy()
    for i, j in kwargs.items():
        selection = selection.loc[(log_file[i]==j)]
    return selection.reset_index(drop=True)

def create_header(row):
    #it iterates over the logfile and looks for the cells that are filled with some value
    #to create the header. It appends a list with the position of the sensors of the filled
    #cells. These headers are used to names of the columns of all the text files.
    try:
        header = ["Date", "Time"]
        for i in range(1,15):
            if row["S"+str(i)] == "":
                continue
            if row["S"+str(i)] != "":
                header.append("s"+str(i))
        return header
    except:
        raise TypeError("Sorry, the header of the files could not be created. Please, review select_files.py")