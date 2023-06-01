import PySimpleGUI as sg

from enums.outputType import OutputType

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
                        sg.Input(visible=True, enable_events=True, key='-INPUT-', size=(30,1)),
                        sg.FilesBrowse(file_types=(("CSV Files","*.csv"),))
                    ],
                    [
                        sg.DropDown(values=[], enable_events=True, key='-CODE-', disabled=True, size=(30,1))
                    ],
                    [
                        sg.Radio(OutputType.POLYGON.getTitleCase(), "GEOMTYPE", enable_events=True, default=True, key='-GEOM_POLYGON-')
                    ],
                    [
                        sg.Radio(OutputType.POINT.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_POINT-', disabled=True)
                    ],
                    [
                        sg.Radio(OutputType.LINE.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_LINE-')
                    ],
                    [
                        sg.Button("Convert", key="-CONVERT-", disabled=True)
                    ],
                    [
                        sg.Button("Close", key="-CLOSE-")
                    ]
                ]

    def initializeGui(self):
        layout = self.createLayout()

        return sg.Window(self.programTitle, layout)
