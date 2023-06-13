import csv
import io

from csvGeom.csvRow import CsvRow
from csvGeom.utils.util import Util

DELIMITER = ','

class InputReader():

    def __init__(self, language, logger):
        self.logger = logger
        self.util = Util()
        self.translations = self.util.loadTranslations(language)

    def parseRow(self, row):
        rowObj = CsvRow()
        try:
            rowObj.id = row['PtID']
            rowObj.east = row['East']
            rowObj.north = row['North']
            
            rowObj.code = row['Code']
            rowObj.identifier = row['Identifier']
        except:
            raise KeyError
        
        try:
            rowObj.height = row['Height']
        except:
            rowObj.height = "0"

        return rowObj

    def createCsvRowList(self, inpFileName):
        with io.open(inpFileName) as impFile:
            rows = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                try:
                    rowObj = self.parseRow(row)
                    rows.append(rowObj)
                except KeyError:
                    self.logger.error(self.translations["err_missingColumn"])
                    break
                
            return rows
        
    def createCodeDropDownEntries(self, rows):
        codes = []

        for obj in rows:
            if obj.code not in codes:
                codes.append(obj.code)

        self.logger.info(self.translations["cli_uniqueCodes"], [len(codes), codes])

        return codes
        
    def filterByCode(self, rows, code):
        list = []

        for obj in rows:
            if obj.code == code:
                list.append(obj)

        self.logger.info(self.translations["cli_filteredByCode"], [code])

        return list
    
    def getAllUniqueIdentifiers(self, lists):
        identifiers = []

        for list in lists:
            identifier = self.util.getIdentifierFromList(list)

            if identifier not in identifiers:
                identifiers.append(identifier)

        self.logger.info(self.translations["cli_uniqueIdentifiers"], [len(identifiers), identifiers])

        return identifiers
    
    def aggregateByIdentifier(self, splitList):
        identifiers = self.getAllUniqueIdentifiers(splitList)

        geometryWrapper = []
        geometryList = []

        for identifier in identifiers:
            for item in splitList:
                if identifier == self.util.getIdentifierFromList(item):
                    geometryWrapper.append(item)
            geometryList.append(geometryWrapper)
            geometryWrapper = []        

        self.logger.info(self.translations["cli_aggregatedGeometries"], [len(geometryList)])

        return geometryList
    
    def splitByIdentifier(self, rows):
        if len(rows) == 0:
            return []
        
        lists = []
        list = []
        lists.append(list)
        
        identifier = self.util.getIdentifierFromList(rows)

        for row in rows:
            if row.identifier == identifier:
                list.append(row)
            else:
                identifier = row.identifier
                list = []
                list.append(row)
                lists.append(list)

        return lists
