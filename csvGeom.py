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

    PROGRAM_TITLE = "csvGeom v0.5.0"

    def __init__(self):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()
        self.argParser = ArgParser()

        self.args = self.argParser.args

        self.rows = None
        self.filteredRows = None
        self.aggregatedData = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.outputFilePath = None

        self.featureCollectionModel = None

        self.gui = None

    def parseGeometryType(self, arg):
        type = None
        try:
            type = OutputType(arg)
        except ValueError:
            self.logger.error(f"Unable to parse GeometryType {arg}. Reverting to default: 'Polygon'.")
            raise ValueError

        return type

    def checkValidCodeSelection(self, entries, selection):
        if selection in entries:
            return True
        else:
            return False

    def handleCli(self):
            self.selectedFileName = self.args.i

            try:
                self.selectedType = self.parseGeometryType(self.args.g)
            except ValueError:
                self.selectedType = OutputType.POLYGON

            self.rows = self.inputReader.createCsvRowList(self.selectedFileName)
            entries = self.inputReader.createCodeDropDownEntries(self.rows)

            while True:
                self.selectedCode = input(f"Found {len(entries)} codes. Please select one of the following: {entries}\n")
                if self.checkValidCodeSelection(entries, self.selectedCode):
                    self.logger.info(f"{self.selectedCode} selected.")
                    break
                else:
                    self.logger.error(f"{self.selectedCode} is not a valid selection. Please try again.")

            self.filteredRows = self.inputReader.filterByCode(self.rows, self.selectedCode)

            splitData = self.inputReader.splitByIdentifier(self.filteredRows)
            self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

            featureCollectionModel = self.modeller.createFeatureCollection(self.aggregatedData, self.selectedType)
            
            output = str(featureCollectionModel)

            self.outputFilePath = self.args.o
            if self.args.o == "":
                self.outputFilePath = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(output, self.outputFilePath)
            else:
                self.writer.writeToFile(output, self.outputFilePath + self.selectedFileType.value)

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.logger.info("File chosen: " + self.selectedFileName)
        self.rows = self.inputReader.createCsvRowList(self.selectedFileName)

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        self.logger.info("Code selected: " + selectedCode)
        self.filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)

    def handleGui(self):
        self.gui = Gui(self.PROGRAM_TITLE, self.args.l)

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
        
    def main(self):

        if self.args.cli:
            self.handleCli()

        else:
            self.handleGui()

if __name__ == '__main__':
    app = Main()
    app.main()
