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

def indent(n):
    indent = '    ' * n # Four spaces times n
    indent = '\n' + indent
    return indent

def convertData(values):
    inpFileName = values['-IN-']
    outputFileName = getFileNameWithoutSuffix(inpFileName)

    dict_list = createDictionary(inpFileName)
    
    data = '{'
    data = data + indent(1) + '"type": "FeatureCollection",' 
    data = data + indent(1) + '"name": "csvGeom-Export",'
    data = data + indent(1) + '"features": [ '

    data = data + createPolygonFeature(dict_list)

    # closing bracket for features + Feature Collection
    data = data + indent(1) + ']' + '\n}'

    writePolygonToFile(outputFileName, data)

# sollte nur 'values' akzeptieren: also schon ein 
def createPoint(values, minIndent, last):
    point = indent(minIndent) + '['
    point = point + indent(minIndent + 1) + values[0] + ','
    point = point + indent(minIndent + 1) + values[1] + ','
    point = point + indent(minIndent + 1) + values[2] + ''
    point = point + indent(minIndent) + ']'
    if last == False: 
        point = point + ','
    
    return point

def createPolygonFeature(dict):
    feature = indent(2) + '{'
    feature = feature + indent(3) + '"type": "Feature",'
    feature = feature + indent(3) + '"properties": {'
    feature = feature + indent(4) + '"identifier": "' + str(dict[0]['Attribut1']) + '"'
    feature = feature + indent(3) + '},'
    feature = feature + indent(3) + '"geometry": {'
    feature = feature + indent(4) + '"type": "Polygon",'
    feature = feature + indent(4) + '"coordinates": ['
    feature = feature + indent(5) + '['

    dict_len = len(dict)

    
    for i in range(dict_len):
        values = [str(dict[i]['East']).replace(' ', ''), str(dict[i]['North']).replace(' ', ''), str(dict[i]['Height']).replace(' ', '')]
        if i+1 == dict_len:
            feature = feature + createPoint(values, 6, True)
        else:
            feature = feature + createPoint(values, 6, False)

    feature = feature + indent(5) + ']'
    feature = feature + indent(4) + ']'
    
    # closing brackets for geometry + single feature
    feature = feature + indent(3) + '}'
    feature = feature + indent(2) + '}'

    return feature

def createLineFeature():
    pass

def createPointFeature(values):
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
