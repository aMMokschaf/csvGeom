from csvGeom.inputReader import InputReader
from csvGeom.modeller import Modeller
from csvGeom.utils.util import Util
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.enums.outputType import OutputType
from csvGeom.enums.fileType import FileType
from csvGeom.utils.logger import Logger

class CsvGeomCli():

    def __init__(self, args):
        self.args = args

        self.util = Util()
        self.translations = self.util.loadTranslations(args.l)
        self.writer = FileWriter(args.l)
        self.logger = Logger()
        self.modeller = Modeller()
        self.inputReader = InputReader(args.l)

        self.selectedFileType = FileType.GEO_JSON

    def parseGeometryType(self, arg):
        type = None
        try:
            type = OutputType(arg)
        except ValueError:
            self.logger.error(self.translations["err_parseGeometry"], [arg])
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
            msg = self.util.createFormattedMsg(self.translations["cli_selectCode"], [len(entries), entries])

            selectedCode = input(msg)
            if self.checkValidCodeSelection(entries, selectedCode):
                self.logger.info(self.translations["cli_codeSelected"], [selectedCode])
                return selectedCode
            else:
                self.logger.error(self.translations["err_invalidCode"], [selectedCode])

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
