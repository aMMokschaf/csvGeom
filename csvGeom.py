# csvGeom v0.1.0

import PySimpleGUI as sg

from gui import Gui
from inputReader import InputReader
from modeller import Modeller
from utils.util import Util
from utils.fileWriter import FileWriter
from enums.outputType import OutputType
from enums.fileType import FileType
from utils.logger import Logger
from outputFormatter import OutputFormatter

class Main():

    PROGRAM_TITLE = "csvGeom v0.1.0"

    def __init__(self):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.dict = []
        self.filteredDict = []

    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        inputReader = InputReader()
        selectedType = OutputType.POLYGON.value
        featureCollectionModel = None

        while True:
            event, values = window.read()

            if event == "-IN-":
                inputFileName = values['-IN-']

                self.dict = inputReader.createDictionary(inputFileName)

                list = inputReader.createDropDownList(self.dict)

                window["CodeSelected"].update(values=list, disabled=False)

                self.logger.info("File chosen: " + inputFileName)

            if event == "CodeSelected":
                selectedCode = values['CodeSelected']
                self.filteredDict = inputReader.filterByCode(self.dict, selectedCode)

                window["Convert"].update(disabled=False)

                self.logger.info("Code selected: " + selectedCode)

                splitData = inputReader.splitByIdentifier(self.filteredDict)

                self.logger.info("Found " + str(len(splitData)) + " objects.", splitData)

                featureCollectionModel = self.modeller.convertInputToModel(splitData, OutputType(selectedType))

                self.logger.info("Converted to object-model.")

            if event == "GeomPolygon":
                selectedType = OutputType.POLYGON.value
                self.logger.info("Output-type selected: " + selectedType)

            if event == "GeomPoint":
                selectedType = OutputType.POINT.value
                self.logger.info("Output-type selected: " + selectedType)

            if event == "Convert":
                
                typeSuffix = OutputType(selectedType).getAsSuffix()
                fileEnding = FileType.GEO_JSON.value
                inputFileName = values['-IN-']
                outputFileName = self.util.getFileNameWithoutSuffix(inputFileName)
                outputFileName = outputFileName + typeSuffix + fileEnding

                data = OutputFormatter().createFeatureCollection(featureCollectionModel)

                self.writer.writeToFile(data, outputFileName)

                self.logger.info("File written: " + outputFileName)

            if event == "Close" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
