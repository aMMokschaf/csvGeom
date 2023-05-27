import PySimpleGUI as sg

from outputType import OutputType

class Gui():
    programTitle = ''

    def __init__(self, programTitle):
        self.programTitle = programTitle

    def createLayout(self):
        return [
                    [
                        sg.Text("Convert Lists of Coordinates to GeoJSON-geometry-Format for Field Desktop")
                    ],
                    [
                        sg.Input(visible=True, enable_events=True, key='-IN-', size=(30,1)),
                        sg.FilesBrowse(file_types=(("CSV Files","*.csv"),))
                    ],
                    [
                        sg.DropDown(values=[], enable_events=True, key='CodeSelected', disabled=True, size=(30,1))
                    ],
                    [
                        sg.Radio('Polygon', "GEOMTYPE", default=True, key='GeomPolygon')
                    ],
                    [
                        sg.Radio('Point', "GEOMTYPE", default=False, key='GeomPoint')
                    ],
                    [
                        sg.Button("Convert", disabled=True)
                    ],
                    [
                        sg.Button("Close")
                    ]
                ]

    def initializeGui(self):
        layout = self.createLayout()

        return sg.Window(self.programTitle, layout)
