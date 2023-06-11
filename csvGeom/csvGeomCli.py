from csvGeom.inputReader import InputReader
from csvGeom.modeller import Modeller
from csvGeom.utils.util import Util
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.enums.outputType import OutputType
from csvGeom.enums.fileType import FileType
from csvGeom.utils.logger import Logger

class CsvGeomCli():

    def __init__(self, args):
        self.util = Util()
        self.writer = FileWriter()
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader()

        self.args = args

        self.selectedFileType = FileType.GEO_JSON

    def parseGeometryType(self, arg):
        type = None
        try:
            type = OutputType(arg)
        except ValueError:
            self.logger.error(f"Unable to parse GeometryType {arg}. Reverting to default: 'Polygon'.")
            type = OutputType.POLYGON

        return type

    def checkValidCodeSelection(self, entries, selection):
        if selection in entries:
            return True
        else:
            return False
        
    def handleCodeSelection(self, entries):
        selectedCode = None
        while True:
            selectedCode = input(f"Found {len(entries)} codes. Please select one of the following: {entries}\n")
            if self.checkValidCodeSelection(entries, selectedCode):
                self.logger.info(f"{selectedCode} selected.")
                return selectedCode
            else:
                self.logger.error(f"{selectedCode} is not a valid selection. Please try again.")

    def handleOutputPath(self, selectedFileName, selectedType):
        outputFilePath = self.args.o

        if self.args.o == "":
            outputFilePath = self.util.createOutputFileName(selectedFileName, selectedType, self.selectedFileType)

        return outputFilePath
                
    def handleCli(self):
            selectedFileName = self.args.i

            selectedType = self.parseGeometryType(self.args.g)

            rows = self.inputReader.createCsvRowList(selectedFileName)

            entries = self.inputReader.createCodeDropDownEntries(rows)

            selectedCode = self.handleCodeSelection(entries)

            filteredRows = self.inputReader.filterByCode(rows, selectedCode)

            splitData = self.inputReader.splitByIdentifier(filteredRows)

            aggregatedData = self.inputReader.aggregateByIdentifier(splitData)

            featureCollectionModel = self.modeller.createFeatureCollection(aggregatedData, selectedType)
            
            output = str(featureCollectionModel)

            outputFilePath = self.handleOutputPath(selectedFileName, selectedType)

            self.writer.writeToFile(output, outputFilePath + self.selectedFileType.value)
