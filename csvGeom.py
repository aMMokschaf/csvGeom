import PySimpleGUI as sg

from gui import Gui
from inputReader import InputReader
from modeller import Modeller
from utils.util import Util
from utils.fileWriter import FileWriter
from enums.outputType import OutputType
from enums.fileType import FileType
from utils.logger import Logger

class Main():

    PROGRAM_TITLE = "csvGeom v0.3.1"

    def __init__(self):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()

        self.rows = []
        self.filteredRows = []
        self.aggregatedData = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.featureCollectionModel = None

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.logger.info("File chosen: " + self.selectedFileName)
        self.rows = self.inputReader.createCsvRowList(self.selectedFileName)

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        self.logger.info("Code selected: " + selectedCode)
        self.filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)
        
    def main(self):

        gui = Gui(self.PROGRAM_TITLE)
        window = gui.initializeGui()

        while True:
            event, values = window.read()

            if event == "-INPUT-":
                self.handleInput(values)

                list = self.inputReader.createDropDownList(self.rows)
                window["-CODE-"].update(values=list, disabled=False)
                window["-CONVERT-"].update(disabled=True)

            if event == "-CODE-":
                self.handleCode(values)

                splitData = self.inputReader.splitByIdentifier(self.filteredRows)
                self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

                window["-CONVERT-"].update(disabled=False)
                self.logger.info(f"Found {str(len(splitData))} objects.")
                self.logger.debug(f"Objects: {splitData}")

            if event == "-GEOM_POINT-":
                self.selectedType = OutputType.POINT
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-GEOM_LINESTRING-":
                self.selectedType = OutputType.LINESTRING
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-GEOM_POLYGON-":
                self.selectedType = OutputType.POLYGON
                self.logger.info("Output-type selected: " + self.selectedType.value)

            if event == "-CONVERT-":
                featureCollectionModel = self.modeller.createFeatureCollection(self.aggregatedData, self.selectedType)
                self.logger.info("Converted to object-model.")
                self.logger.debug(f"Object-Model: {featureCollectionModel}")
                self.logger.debug(featureCollectionModel.features)
                
                output = str(featureCollectionModel)

                outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(output, outputFileName)

            if event == "-CLOSE-" or event == sg.WIN_CLOSED:
                break

        window.close()

if __name__ == '__main__':
    app = Main()
    app.main()
