import os
import re
import sys
import logging
import tkinter
from tkinter import filedialog
import pandas as pd


def report_csv(data,d_path):
    for elm in data:
        writer = pd.ExcelWriter(f'{d_path}/{elm}.xlsx', engine='xlsxwriter')
        for page in data[elm]:
            temp = pd.DataFrame(
                {
                    "X": page["table"]["x"],
                    "Y": page["table"]["y"],
                    "area": page["peak_table"]["area"],
                    "height": page["peak_table"]["height"],
                    "a/h": page["peak_table"]["a/h"]
                }
            )
            temp.to_excel(writer, sheet_name=f"{page['temp']}")
        writer.save()
    exit(0)


def read_file(name):
    file_name = re.search(r"([a-zA-Z])+?_([0-9])+", os.path.split(name)[1]).group(0).split("_")
    dict_ = {
        "table":
            {
                "x": [],
                "y": [],
                "y'": []
            },
        "peak_table": {
            "area": 0,
            "height": 0,
            "a/h": 0
        },
        "name": file_name[0],
        "temp": file_name[1],
        "y_max": 0
    }
    with open(name, "r") as file:
        data = file.read()
        for elm in re.finditer(r"[0-9],([0-9]){0,5}\t([\-]){0,1}([0-9])+?\n", data):
            line = re.split(r'\t', elm.group(0))
            dict_["table"]["x"].append(format(float(line[0].rstrip().replace(",", ".")), '.5f'))
            dict_["table"]["y"].append(int(line[1].rstrip()))
            if dict_["y_max"] < int(line[1].rstrip()):
                dict_["y_max"] = int(line[1].rstrip())
        other_data = re.search(r"2\t([^a-z])+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t", data).group(0).split("\t")
        print(f"area:{other_data[4]},heihg:{other_data[5]},a/h:{other_data[6]}")
        try:
            dict_["peak_table"]["area"] = float(format(float(other_data[4].replace(",", ".")), '.5f'))
            dict_["peak_table"]["height"] = float(format(float(other_data[5].replace(",", ".")), '.5f'))
            dict_["peak_table"]["a/h"] = float(format(float(other_data[6].replace(",", ".")), '.5f'))
        except ValueError:
            logging.error(file_name)
    return dict_


def read_directoy(path, d_path):
    data = []
    tmp = {}
    for thing in os.listdir(path):
        data.append(read_file(f"{path}/{thing}"))
    for thing in data:
        if thing["name"] in tmp:
            tmp[thing["name"]].append(thing)
        else:
            tmp[thing["name"]] = [thing]
    report_csv(tmp, d_path)


def tk_file():
    file = filedialog.askopenfilename()
    read_file(file)


def tk_dir():
    path = filedialog.askdirectory()
    d_path = filedialog.askdirectory()
    read_directoy(path, d_path)


if __name__ == '__main__':
    # read_file("C:/Users/flori/PycharmProjects/CASC-calc/doc/1-Butanol_70°.TXT")
    # read_directoy("C:/Users/flori/PycharmProjects/CASC-calc/doc/")
    # report_csv("")
    # exit(1)
    if sys.version_info.major == 3:
        root = tkinter.Tk()
        file = tkinter.Button(root, text="Read file...", command=tk_file)
        dirs = tkinter.Button(root, text="Open directory...", command=tk_dir)
        file.pack()
        dirs.pack()
        root.mainloop()
    else:
        print(f"Please User Python3")

# [0-9],([0-9]){0,5}\t([\-]){0,1}[0-9]/g R.Time Intensity
