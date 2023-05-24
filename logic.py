import csv
import io

from fileType import FileType
from outputType import OutputType
from util import Util
from converter import Converter
from fileWriter import FileWriter

DELIMITER = ','

class Logic(): #Rename to something about input

    util = None
    converter = None

    def __init__(self):
        self.util = Util()
        self.converter = Converter()

    def createDictionary(self, inpFileName):
        with io.open(inpFileName) as impFile:
            dict = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                dict.append(row)

            return dict
        
    def createDropDownList(self, dict): #
        pass
        #iterate over dict and create list of unique codes like 'Befund'
        
    def filterByCode(self, code): 
        pass
        #iterate over dict and create a new dict only with only the right entries

    def convertData(self, dict):
        return self.converter.createFeatureCollection(dict)
