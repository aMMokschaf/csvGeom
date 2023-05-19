# csvGeom v0.1.0

import PySimpleGUI as sg
import csv
import io

DELIMITER = ','
PROGRAM_TITLE = "csvGeom v0.1.0"
FILE_SUFFIX = "_polygon.txt"

layout = [
    [
        sg.Text("Convert Lists of Coordinates to GeoJSON-geometry-Format for Field Desktop")
    ],
    [
        sg.Input(visible=True, enable_events=True, key='-IN-'),
        sg.FilesBrowse(file_types=(("CSV Files","*.csv"),))
    ], 
    [
        sg.Button("Convert")
    ],
    [
        sg.Button("Close")
    ]
]

window = sg.Window(PROGRAM_TITLE, layout)

while True:
    event, values = window.read()

    if event == "Convert":
        inpfilename = values['-IN-']
        inpnewfilename = inpfilename.replace('.csv', '')

        with io.open(str(inpfilename)) as impfile:
            dict_list = []
            reader = csv.DictReader(impfile, delimiter=DELIMITER)
            for row in reader:
                dict_list.append(row)

        file = io.open(str(inpnewfilename + FILE_SUFFIX), "w")

        dict_len = len(dict_list)

        file.write("[\n    [\n")
        for i in range(dict_len):
            file.write("        [\n")
            file.write("            " + str(dict_list[i]['East']).replace(' ', '') + ",\n")
            file.write("            " + str(dict_list[i]['North']).replace(' ', '') + ",\n")
            file.write("            " + str(dict_list[i]['Height']).replace(' ', '') + "\n")
            if i+1 == dict_len:
                file.write("        ]\n")
            else:
                file.write("        ],\n")
        file.write("    ]\n]")

        file.close()

    if event == "Close" or event == sg.WIN_CLOSED:
        break

window.close()

