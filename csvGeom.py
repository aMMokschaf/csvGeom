import PySimpleGUI as sg

from gui import Gui
from inputReader import InputReader
from modeller import Modeller
from utils.util import Util
from utils.fileWriter import FileWriter
from enums.outputType import OutputType
from enums.fileType import FileType
from utils.logger import Logger
from utils.argParser import ArgParser

class Main():

    PROGRAM_TITLE = "csvGeom v0.3.5"

    def __init__(self):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()
        self.argParser = ArgParser()

        self.args = self.argParser.args

        self.rows = []
        self.filteredRows = []
        self.aggregatedData = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.featureCollectionModel = None

        self.gui = Gui(self.PROGRAM_TITLE, self.args.l)

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.logger.info("File chosen: " + self.selectedFileName)
        self.rows = self.inputReader.createCsvRowList(self.selectedFileName)

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        self.logger.info("Code selected: " + selectedCode)
        self.filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)
        
    def main(self):

        if self.args.cli:
            self.logger.debug("Using CLI")
        else:
            while True:
                event, values = self.gui.readValues()

                if event == "-INPUT-":
                    self.handleInput(values)

                    entries = self.inputReader.createCodeDropDownEntries(self.rows)
                    self.gui.updateValues("-CODE-", entries)
                    self.gui.enableElement("-CODE-")

                    self.gui.disableElement("-CONVERT-")

                if event == "-CODE-":
                    self.handleCode(values)

                    splitData = self.inputReader.splitByIdentifier(self.filteredRows)
                    self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

                    self.gui.enableElement("-CONVERT-")
                    self.logger.info(f"Found {str(len(splitData))} objects.")

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
                    
                    output = str(featureCollectionModel)

                    outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                    self.writer.writeToFile(output, outputFileName)

                if event == "-CLOSE-" or event == sg.WIN_CLOSED:
                    break

            self.gui.destroy()


if __name__ == '__main__':
    app = Main()
    app.main()
