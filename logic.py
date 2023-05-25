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
        
    def createDropDownList(self, dict):
        list = []

        for obj in dict:
            if obj['Code'] not in list:
                list.append(obj['Code'])

        return list
        
    def filterByCode(self, dict, code):
        list = []

        for obj in dict:
            if obj['Code'] == code:
                print(obj)
                list.append(obj)

        return list

    def convertData(self, dict, selectedType):
        return self.converter.createFeatureCollection(dict, selectedType)
