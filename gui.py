import PySimpleGUI as sg

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

    def initializeGui(self):
        layout = self.createLayout()

        return sg.Window(self.programTitle, layout)
