# csvGeom v0.1.0

import PySimpleGUI as sg
import csv
import io


# layout of the window
layout = [[sg.Text("Convert Lists of Coordinates to GeoJSON-geometry-Format for Field Desktop")], [sg.Input(visible=True, enable_events=True, key='-IN-'), sg.FilesBrowse(file_types=(("CSV Files","*.csv"),))], 
[sg.Button("Convert")],[sg.Button("Close")]]

# settings of window
window = sg.Window("csvGeom v0.1.0", layout)

# event loop 
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the "Close" button
    if event == "Convert":
        inpfilename = values['-IN-']
        inpnewfilename = inpfilename.replace('.csv', '')
        with io.open(str(inpfilename)) as impfile:
            dict_list = []
            reader = csv.DictReader(impfile, delimiter=',')
            for row in reader:
                dict_list.append(row)
        #Schreibt alles in eine Datei, iteriert über die Listeneinträge / Reihen
        file = io.open(str(inpnewfilename+"_polygon.txt"), "w")

        file.write("[\n    [\n")
        for i in range(len(dict_list)):
            file.write("        [\n")
            file.write("            "+str(dict_list[i]['East']).replace(' ', '')+",\n")
            file.write("            "+str(dict_list[i]['North']).replace(' ', '')+",\n")
            file.write("            "+str(dict_list[i]['Height']).replace(' ', '')+"\n")
            if i+1 == len(dict_list):
                file.write("        ]\n")
            else:
                file.write("        ],\n")
        file.write("    ]\n]")
        file.close() 

    if event == "Close" or event == sg.WIN_CLOSED:
        break

window.close()
