import csv
import io

from utils.logger import Logger

DELIMITER = ','

class InputReader():

    def __init__(self):
        self.logger = Logger()

    def createDictionary(self, inpFileName):
        with io.open(inpFileName) as impFile:
            dict = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                dict.append(row)

            return dict
        
    def createDropDownList(self, dict):
        codes = []

        for obj in dict:
            if obj['Code'] not in codes:
                codes.append(obj['Code'])

        self.logger.info(f"Found {len(codes)} unique codes: {codes}")

        return codes
        
    def filterByCode(self, dict, code):
        list = []

        for obj in dict:
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
    
    def aggregateByIdentifier(self, splitDict):
        identifiers = self.getAllUniqueIdentifiers(splitDict)

        geometryWrapper = []
        geometryList = []

        for identifier in identifiers:
            for item in splitDict:
                if identifier == item[0]['Attribut1']:
                    geometryWrapper.append(item)
            geometryList.append(geometryWrapper)
            geometryWrapper = []        

        self.logger.info(f"Aggregated {len(geometryList)} geometries.")
        self.logger.debug(f"Aggregated geometries: {geometryList}")

        return geometryList
    
    def splitByIdentifier(self, dict):
        if len(dict) == 0:
            return []
        
        lists = []
        list = []
        lists.append(list)
        
        identifier = dict[0]['Attribut1']

        for obj in dict:
            if obj['Attribut1'] == identifier:
                list.append(obj)
            else:
                identifier = obj['Attribut1']
                list = []
                list.append(obj)
                lists.append(list)

        return lists
