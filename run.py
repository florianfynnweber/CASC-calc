import csv
import os
import sys
import tkinter
from pprint import pprint
from tkinter import filedialog
import pandas as pd


# b und d
def read_file(file, d_path):
    xls = pd.ExcelFile(file)
    # print(xls)
    sheets = []
    tmp = []
    tmpm1 = {}
    for sheet in xls.sheet_names:
        df = pd.read_excel(xls, sheet, index_col=None, na_values=["N/A"])
        # print(df.to_dict(orient="record"))
        datas = df.to_dict(orient="record")
        sheets.append(datas)
        for thing in datas:
            if "X " in thing:
                coord = [thing["X "], thing[list(thing.keys())[3]]]
            else:
                coord = [thing["X"], thing[list(thing.keys())[3]]]
            tmp.append(coord)
        #tmpm1[sheet] = tmp
        #print(tmp)
        with open(os.path.join(d_path,f"{sheet}.csv"), "w") as file:
            writer = csv.writer(file)
            writer.writerows(tmp)
    return tmpm1


def tk_file():
    file = filedialog.askopenfilename()
    d_path = filedialog.askdirectory()
    data = read_file(file, d_path)
    for sheet in data:
        print(sheet)

def tk_dir():
    path = filedialog.askdirectory()
    data = []
    tmp = {}
    for thing in os.listdir(path):
        data.append(read_file(f"{path}/{thing}"))


if sys.version_info.major == 3:
    read_file("C:/Users/flori/PycharmProjects/CASC-calc/doc/Butanol.xlsx","C:/Users/flori/PycharmProjects/CASC-calc/")
    exit(0)
    root = tkinter.Tk()
    file = tkinter.Button(root, text="Read file...", command=tk_file)
    dirs = tkinter.Button(root, text="Open directory...", command=tk_dir)
    file.pack()
    dirs.pack()
    root.mainloop()
else:
    print(f"Please User Python3")


"""
with open("files/csv1.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        # convert tuple to dictionary
        print(dict(row))
"""