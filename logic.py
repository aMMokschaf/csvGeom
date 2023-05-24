import csv
import io

from fileType import FileType
from util import Util
from converter import Converter
from fileWriter import FileWriter

DELIMITER = ','

class Logic():

    util = None
    converter = None
    writer = None

    def __init__(self):
        self.util = Util()
        self.converter = Converter()
        self.writer = FileWriter()

    def createDictionary(self, inpFileName):
        with io.open(inpFileName) as impFile:
            dict = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                dict.append(row)

            return dict

    def convertData(self, values):
        inputFileName = values['-IN-']

        outputFileName = self.util.getFileNameWithoutSuffix(inputFileName)

        dict = self.createDictionary(inputFileName)

        data = self.converter.createFeatureCollection(dict)

        self.writer.writePolygonToFile(outputFileName, data, FileType.GEO_JSON.value)
