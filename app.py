import os
import re
import sys
import logging
import csv
import json
import argparse
import tkinter
from pprint import pprint
from tkinter import filedialog
import pandas as pd
import xlsxwriter


# main minimal gui tkinter explrer stuff

def report_csv(data):
    for elm in data:
        writer = pd.ExcelWriter(f'{elm}.xlsx', engine='xlsxwriter')
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
    # df1 = pd.DataFrame({'Data': [11, 12, 13, 14]})
    # df2 = pd.DataFrame({'Data': [21, 22, 23, 24]})
    # df3 = pd.DataFrame({'Data': [31, 32, 33, 34]})
    # writer = pd.ExcelWriter('pandas_multiple.xlsx', engine='xlsxwriter')
    # df1.to_excel(writer, sheet_name='Sheet1')
    # df2.to_excel(writer, sheet_name='Sheet2')
    # df3.to_excel(writer, sheet_name='Sheet3')
    # temp.to_excel(writer, sheet_name='Sheet4')


def read_file(name):
    file_name = re.search("([a-zA-Z])+?_([0-9])+", os.path.split(name)[1]).group(0).split("_")
    dict_ = {
        "table":
            {
                "x": [],
                "y": []
            },
        "peak_table": {
            "area": "",
            "height": "",
            "a/h": ""
        },
        "name": file_name[0],
        "temp": file_name[1]
    }
    with open(name, "r") as file:
        data = file.read()
        for elm in re.finditer("[0-9],([0-9]){0,5}\t([\-]){0,1}([0-9])+?\n", data):
            line = re.split(r'\t', elm.group(0))
            dict_["table"]["x"].append(format(float(line[0].rstrip().replace(",", ".")), '.5f'))
            dict_["table"]["y"].append(int(line[1].rstrip()))
        other_data = re.search("2\t([^a-z])+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t(.)+?\t", data).group(0).split("\t")
        print(f"area:{other_data[4]},heihg:{other_data[5]},a/h:{other_data[6]}")
        try:
            dict_["peak_table"]["area"] =format(float(other_data[4].replace(",",".")),'.5f')
            dict_["peak_table"]["height"] = format(float(other_data[5].replace(",",".")),'.5f')
            dict_["peak_table"]["a/h"] = format(float(other_data[6].replace(",",".")),'.5f')
        except ValueError:
            logging.error(file_name)
    return dict_


def read_directoy(path):
    data = []
    tmp = {}
    for thing in os.listdir(path):
        data.append(read_file(f"{path}/{thing}"))
    for thing in data:
        if thing["name"] in tmp:
            tmp[thing["name"]].append(thing)
        else:
            tmp[thing["name"]] = [thing]
    report_csv(tmp)


def tk_file():
    file = filedialog.askopenfilename()
    read_file(file)


def tk_dir():
    path = filedialog.askdirectory()
    read_directoy(path)


if __name__ == '__main__':
    # read_file("C:/Users/flori/PycharmProjects/CASC-calc/doc/1-Butanol_70°.TXT")
    read_directoy("C:/Users/flori/PycharmProjects/CASC-calc/doc/")
    # report_csv("")
    exit(1)
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
