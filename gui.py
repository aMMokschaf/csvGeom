import PySimpleGUI as sg

from utils.util import Util

from enums.outputType import OutputType

class Gui():

    def __init__(self, programTitle, language):
        self.programTitle = programTitle
        self.util = Util()
        self.translations = self.util.loadTranslations(language)
        self.layout = self.createLayout()
        self.window = sg.Window(self.programTitle, self.layout)

    def createLayout(self):
        return [
                    [
                        sg.Text(self.translations["gui_header"])
                    ],
                    [
                        sg.Input(visible=True, enable_events=True, key='-INPUT-', size=(30,1)),
                        sg.FilesBrowse(self.translations["gui_browse"], file_types=(("CSV Files","*.csv"),))
                    ],
                    [
                        sg.DropDown(values=[], enable_events=True, key='-CODE-', disabled=True, size=(30,1))
                    ],
                    [
                        sg.Radio(OutputType.POLYGON.getTitleCase(), "GEOMTYPE", enable_events=True, default=True, key='-GEOM_POLYGON-')
                    ],
                    [
                        sg.Radio(OutputType.POINT.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_POINT-')
                    ],
                    [
                        sg.Radio(OutputType.LINESTRING.getTitleCase(), "GEOMTYPE", enable_events=True, default=False, key='-GEOM_LINESTRING-')
                    ],
                    [
                        sg.Button(self.translations["gui_convert"], key="-CONVERT-", disabled=True)
                    ],
                    [
                        sg.Button(self.translations["gui_close"], key="-CLOSE-")
                    ]
                ]
    
    def enableElement(self, element):
        self.window[element].update(disabled=False)

    def disableElement(self, element):
        self.window[element].update(disabled=True)
    
    def updateValues(self, element, values):
        self.window[element].update(values=values)

    def readValues(self):
        return self.window.read()

    def destroy(self):
        self.window.close()
