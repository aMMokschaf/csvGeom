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
        self.inputReader = InputReader()

        self.dict = []
        self.filteredDict = []

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.featureCollectionModel = None

    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        while True:
            event, values = window.read()

            if event == "-IN-":
                self.selectedFileName = values['-IN-']
                self.logger.info("File chosen: " + self.selectedFileName)
                self.dict = self.inputReader.createDictionary(self.selectedFileName)

                list = self.inputReader.createDropDownList(self.dict)
                window["CodeSelected"].update(values=list, disabled=False)

            if event == "CodeSelected":
                selectedCode = values['CodeSelected']
                self.filteredDict = self.inputReader.filterByCode(self.dict, selectedCode)
                self.logger.info("Code selected: " + selectedCode)

                splitData = self.inputReader.splitByIdentifier(self.filteredDict)

                window["Convert"].update(disabled=False)
                self.logger.info(f"Found {str(len(splitData))} objects.", splitData)

            if event == "GeomPoint":
                self.selectedType = OutputType.POINT.value
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "GeomPolygon":
                self.selectedType = OutputType.POLYGON
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "Convert":
                featureCollectionModel = self.modeller.convertInputToModel(splitData, self.selectedType)
                self.logger.info("Converted to object-model.")

                data = OutputFormatter().createFeatureCollection(featureCollectionModel)

                outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(data, outputFileName)
                self.logger.info("File written: " + outputFileName)

            if event == "Close" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
