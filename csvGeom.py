# csvGeom v0.1.0

import PySimpleGUI as sg
import csv
import io

DELIMITER = ','
PROGRAM_TITLE = "csvGeom v0.1.0"
OUTPUT_FORMAT = ".geojson"
OUTPUT_SUFFIX_POLYGON = "_polygon" + OUTPUT_FORMAT
OUTPUT_SUFFIX_LINE = "_line" + OUTPUT_FORMAT
OUTPUT_SUFFIX_POINT = "_point" + OUTPUT_FORMAT
TAB = "    " # Four spaces

def createLayout():
    return [
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

def initializeGui():
    layout = createLayout()

    return sg.Window(PROGRAM_TITLE, layout)

def createDictionary(inpFileName):
    with io.open(str(inpFileName)) as impFile:
        dict_list = []
        reader = csv.DictReader(impFile, delimiter=DELIMITER)
        for row in reader:
            dict_list.append(row)
        return dict_list
    
def getFileNameWithoutSuffix(filename):
    return filename.rsplit(".", 1)[0]

def convertData(values):
    inpFileName = values['-IN-']
    outputFileName = getFileNameWithoutSuffix(inpFileName)

    dict_list = createDictionary(inpFileName)
           
    data = createPolygon(dict_list)

    writePolygonToFile(outputFileName, data)

def createPolygon(dict):
    data = '{\n"type": "FeatureCollection",\n"name": "csvGeom-Export",\n'
    data = data +'"features": [ {\n"type": "Feature",\n'
    data = data +'"properties": {\n"identifier": "'+str(dict[0]['Attribut1'])+'"\n},\n'
    data = data +'"geometry": { "type": "Polygon",\n'
    data = data +'"coordinates": \n[\n' + TAB + '[\n'

    dict_len = len(dict)

    for i in range(dict_len):
        data = data + TAB + TAB + "[\n"
        data = data + TAB + TAB + TAB + str(dict[i]['East']).replace(' ', '') + ",\n"
        data = data + TAB + TAB + TAB + str(dict[i]['North']).replace(' ', '') + ",\n"
        data = data + TAB + TAB + TAB + str(dict[i]['Height']).replace(' ', '') + "\n"
        if i+1 == dict_len:
            data = data + TAB + TAB + "]\n"
        else:
            data = data + TAB + TAB + "],\n"
    data = data + TAB + "]\n]"
    
    data = data + "} }]}"

    return data

def createLine():
    pass

def createPoint():
    pass

def writePolygonToFile(filename, data):
    writeToFile(filename, data, OUTPUT_SUFFIX_POLYGON)

def writeLineToFile():
    pass

def writePointToFile():
    pass

def writeToFile(filename, data, suffix):
    file = io.open(filename + suffix, "w")
    file.write(data)
    file.close()

def main():
    
    window = initializeGui()

    while True:
        event, values = window.read()

        if event == "Convert":
            convertData(values)

        if event == "Close" or event == sg.WIN_CLOSED:
            break

    window.close()

if __name__ == '__main__':
    main()
