import PySimpleGUI as sg

from csvGeom.gui import Gui
from csvGeom.inputReader import InputReader
from csvGeom.modeller import Modeller
from csvGeom.utils.util import Util
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.enums.outputType import OutputType
from csvGeom.enums.fileType import FileType

class CsvGeomGui():

    def __init__(self, args):
        self.args = args

        self.util = Util()
        self.writer = FileWriter(args.l)
        self.modeller = Modeller()
        self.inputReader = InputReader(args.l)

        self.rows = None
        self.aggregatedData = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.gui = Gui("csvGeom v0.5.1", self.args.l)

    def handleInput(self, values):
        self.selectedFileName = values['-INPUT-']
        self.rows = self.inputReader.createCsvRowList(self.selectedFileName)

        entries = self.inputReader.createCodeDropDownEntries(self.rows)
        self.gui.updateValues("-CODE-", entries)
        self.gui.enableElement("-CODE-")

        self.gui.disableElement("-CONVERT-")

    def handleCode(self, values):
        selectedCode = values['-CODE-']
        filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)

        splitData = self.inputReader.splitByIdentifier(filteredRows)
        self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

        self.gui.enableElement("-CONVERT-")

    def handleConvert(self):
        featureCollectionModel = self.modeller.createFeatureCollection(self.aggregatedData, self.selectedType)
        
        output = str(featureCollectionModel)

        outputFileName = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
        
        self.writer.writeToFile(output, outputFileName)

    def handleGui(self):
        
        while True:
            event, values = self.gui.readValues()

            if event == "-INPUT-":
                self.handleInput(values)

            if event == "-CODE-":
                self.handleCode(values)

            if event == "-GEOM_POINT-":
                self.selectedType = OutputType.POINT

            if event == "-GEOM_LINESTRING-":
                self.selectedType = OutputType.LINESTRING

            if event == "-GEOM_POLYGON-":
                self.selectedType = OutputType.POLYGON

            if event == "-CONVERT-":
                self.handleConvert()

            if event == "-CLOSE-" or event == sg.WIN_CLOSED:
                break

        self.gui.destroy()       
