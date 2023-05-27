# csvGeom v0.1.0

import PySimpleGUI as sg

from gui import Gui
from logic import Logic
from util import Util
from converter import Converter
from fileWriter import FileWriter
from outputType import OutputType
from fileType import FileType
from logger import Logger

class Main():

    PROGRAM_TITLE = "csvGeom v0.1.0"
    dict = []
    filteredDict = []

    def __init__(self):
        self.util = Util()
        self.converter = Converter()
        self.writer = FileWriter()
        self.logger = Logger()

    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        logic = Logic()

        while True:
            event, values = window.read()

            if event == "-IN-":
                inputFileName = values['-IN-']

                self.dict = logic.createDictionary(inputFileName)

                list = logic.createDropDownList(self.dict)

                window["CodeSelected"].update(values=list, disabled=False)

                self.logger.info("File chosen: " + inputFileName)

            if event == "CodeSelected":
                selectedCode = values['CodeSelected']
                self.filteredDict = logic.filterByCode(self.dict, selectedCode)

                window["Convert"].update(disabled=False)

                self.logger.info("Code selected: " + selectedCode)

            if event == "Convert":
                outputTypeSelection = {
                    "polygon": values['GeomPolygon'],
                    "point": values['GeomPoint'],
                    "linestring": False
                }

                for geomType, selection in outputTypeSelection.items():
                    if selection == True:
                        selectedType = geomType
                
                typeSuffix = OutputType(selectedType).getAsSuffix()
                fileEnding = FileType.GEO_JSON.value
                inputFileName = values['-IN-']
                outputFileName = self.util.getFileNameWithoutSuffix(inputFileName)
                outputFileName = outputFileName + typeSuffix + fileEnding

                data = logic.convertData(self.filteredDict, selectedType)

                self.writer.writeToFile(data, outputFileName)

                self.logger.info("File written: " + outputFileName)

            if event == "Close" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
