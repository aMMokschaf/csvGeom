import PySimpleGUI as sg

from outputType import OutputType

class Gui():
    programTitle = ''
    listOfCodes = []

    def __init__(self, programTitle):
        self.programTitle = programTitle

    def setListOfCodes(self, list):
        self.listOfCodes = list
        # Muss man das aktualisieren?

    def createLayout(self):
        return [
                    [
                        sg.Text("Convert Lists of Coordinates to GeoJSON-geometry-Format for Field Desktop")
                    ],
                    [
                        sg.Input(visible=True, enable_events=True, key='-IN-'),
                        sg.FilesBrowse(file_types=(("CSV Files","*.csv"),))
                    ],
                    [
                        sg.DropDown(self.listOfCodes, enable_events=True, key='CodeSelected')
                    ],
                    [
                        sg.Button("Convert")
                    ],
                    [
                        sg.Button("Close")
                    ]
                ]

    def initializeGui(self):
        layout = self.createLayout()

        return sg.Window(self.programTitle, layout)
