from inputReader import InputReader
from modeller import Modeller
from utils.util import Util
from utils.fileWriter import FileWriter
from enums.outputType import OutputType
from enums.fileType import FileType
from utils.logger import Logger

class CsvGeomCli():

    PROGRAM_TITLE = "csvGeom v0.5.0"

    def __init__(self, args):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()

        self.args = args

        self.rows = None
        self.aggregatedData = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

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

            selectedCode = None
            while True:
                selectedCode = input(f"Found {len(entries)} codes. Please select one of the following: {entries}\n")
                if self.checkValidCodeSelection(entries, selectedCode):
                    self.logger.info(f"{selectedCode} selected.")
                    break
                else:
                    self.logger.error(f"{selectedCode} is not a valid selection. Please try again.")

            filteredRows = self.inputReader.filterByCode(self.rows, selectedCode)

            splitData = self.inputReader.splitByIdentifier(filteredRows)
            self.aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

            featureCollectionModel = self.modeller.createFeatureCollection(self.aggregatedData, self.selectedType)
            
            output = str(featureCollectionModel)

            outputFilePath = self.args.o
            if self.args.o == "":
                outputFilePath = self.util.createOutputFileName(self.selectedFileName, self.selectedType, self.selectedFileType)
                self.writer.writeToFile(output, outputFilePath)
            else:
                self.writer.writeToFile(output, outputFilePath + self.selectedFileType.value)
