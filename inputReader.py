import csv
import io

from utils.logger import Logger

DELIMITER = ','

class InputReader():

    def __init__(self):
        self.logger = Logger()

    def createCsvRowList(self, inpFileName):
        with io.open(inpFileName) as impFile:
            rows = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                rows.append(row)

            return rows
        
    def createDropDownList(self, rows):
        codes = []

        for obj in rows:
            if obj['Code'] not in codes:
                codes.append(obj['Code'])

        self.logger.info(f"Found {len(codes)} unique codes: {codes}")

        return codes
        
    def filterByCode(self, rows, code):
        list = []

        for obj in rows:
            if obj['Code'] == code:
                list.append(obj)

        self.logger.info(f"Filtered by code {code}.")

        return list
    
    def getAllUniqueIdentifiers(self, lists):
        identifiers = []

        for list in lists:
            identifier = list[0]['Attribut1']

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
                if identifier == item[0]['Attribut1']:
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
        
        identifier = rows[0]['Attribut1']

        for row in rows:
            if row['Attribut1'] == identifier:
                list.append(row)
            else:
                identifier = row['Attribut1']
                list = []
                list.append(row)
                lists.append(list)

        return lists
