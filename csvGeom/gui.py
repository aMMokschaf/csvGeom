import PySimpleGUI as sg

from csvGeom.utils.util import Util

from csvGeom.enums.outputType import OutputType

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
                        sg.Graph((700, 50), (0, 0), (700, 50), background_color='white', key='errRectangle')
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
    
    def resetErrMsg(self):
        self.window["errRectangle"].update(background_color='white')
        self.window["errRectangle"].erase()
    
    def updateErrMsg(self, count):
        color = 'white'
        if count > 0:
            color = 'red'
            errMsg = self.translations["gui_error_validation"]
            formattedMsg = self.util.createFormattedMsg(errMsg, [count])

            self.window["errRectangle"].draw_text(formattedMsg, (350, 25), color='black')
        else:
            color = "green"

        self.window["errRectangle"].update(background_color=color)

    def destroy(self):
        self.window.close()
