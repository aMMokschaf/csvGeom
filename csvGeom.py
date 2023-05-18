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
        file = io.open(str(inpnewfilename+"_polygon.geojson"), "w")

        # Zeile für die FeatureCollection, braucht man nur ein mal
        file.write('{\n"type": "FeatureCollection",\n "name": "csvGeom-Export",\n')

        # Start eines Features (= ein Befund = ein Polygon, d.h. im späteren loop(?) braucht man das für jeden unerschiedlichen Wert in der Attributspalte)
        # also muss dann hier eigentlich der (erste) loop (oder was auch immer) anfangen. (das geht bestimmt dynamischer und besser als loopen, aber das ganze war eher improvisiert und nicht notwendigerweise durchdacht)
        file.write('"features": [ {\n"type": "Feature",\n')
        # Der "Name" des Befundes als identifier in den properties des einzelnen Features
        # äh, [0] ist offensichtlich improvisierter müll, weil gerade noch nur eine Datei mit nur einem Befund eingelesen wird.
        file.write('"properties": {\n"identifier": "'+str(dict_list[0]['Attribut1'])+'"\n},\n')
        # die Geometrie/die Koordinaten brauchen einen Type, hier: Polygon, später das, was man halt auswählt
        file.write('"geometry": { "type": "Polygon",\n')
        # hier dann der anfang vom Polygon
        file.write('"coordinates":\n [\n[\n')

        # Zeilen 36-hier kann man dann theoretisch auch in einer Zeile abhandeln, ich persönlich finde das dann aber unverständlich und übersichtlich, also lieber so und dann vermutlich langsamer als völlig undurchsichtig

        # jetz über die einzelnen koordinaten iterieren, jede wird ein punkt im Polygon
        for i in range(len(dict_list)):
            file.write("        [\n")
            file.write("            "+str(dict_list[i]['East']).replace(' ', '')+",\n")
            file.write("            "+str(dict_list[i]['North']).replace(' ', '')+",\n")
            file.write("            "+str(dict_list[i]['Height']).replace(' ', '')+"\n")
            # wenn wir in der letzten Zeile sind kein Komma
            if i+1 == len(dict_list):
                file.write("        ]\n")
            # wenn nicht doch ein Komma
            else:
                file.write("        ],\n")
        # schließende Klammern für das Polygon
        file.write("    ]\n]")
        # schließende Klammern für das JSON-gedönse oben
        file.write("} }]}")
        # schließen weil fertig
        file.close() 

    if event == "Close" or event == sg.WIN_CLOSED:
        break

window.close()
