import csv
import io

from utils.logger import Logger
from csvRow.csvRow import CsvRow

DELIMITER = ','

class InputReader():

    def __init__(self):
        self.logger = Logger()

    def parseRow(self, row):
        rowObj = CsvRow()
        try:
            rowObj.id = row['PtID']
            rowObj.east = row['East']
            rowObj.north = row['North']
            rowObj.height = row['Height']
            rowObj.code = row['Code']
            rowObj.identifier = row['Identifier']
        except:
            raise KeyError

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
                    self.logger.error("Could not find all columns needed to process the file.")
                    break
                
            return rows
        
    def createDropDownList(self, rows):
        codes = []

        for obj in rows:
            if obj.code not in codes:
                codes.append(obj.code)

        self.logger.info(f"Found {len(codes)} unique codes: {codes}")

        return codes
        
    def filterByCode(self, rows, code):
        list = []

        for obj in rows:
            if obj.code == code:
                list.append(obj)

        self.logger.info(f"Filtered by code {code}.")

        return list
    
    def getAllUniqueIdentifiers(self, lists):
        identifiers = []

        for list in lists:
            identifier = list[0].identifier

            if identifier not in identifiers:
                identifiers.append(identifier)

        self.logger.info(f"Found {len(identifiers)} unique identifiers: {identifiers}")

        return identifiers
    
    def aggregateByIdentifier(self, splitList):
        identifiers = self.getAllUniqueIdentifiers(splitList)

        geometryWrapper = []
        geometryList = []

        for identifier in identifiers:
            for item in splitList:
                if identifier == item[0].identifier:
                    geometryWrapper.append(item)
            geometryList.append(geometryWrapper)
            geometryWrapper = []        

        self.logger.info(f"Aggregated {len(geometryList)} geometries.")
        self.logger.debug(f"Aggregated geometries: {geometryList}")

        return geometryList
    
    def splitByIdentifier(self, rows):
        if len(rows) == 0:
            return []
        
        lists = []
        list = []
        lists.append(list)
        
        identifier = rows[0].identifier

        for row in rows:
            if row.identifier == identifier:
                list.append(row)
            else:
                identifier = row.identifier
                list = []
                list.append(row)
                lists.append(list)

        return lists
