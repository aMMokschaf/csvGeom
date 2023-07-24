from csvGeom.utils.util import Util
from csvGeom.enums.outputType import OutputType

class Aggregator():

    def __init__(self, language, logger):
        self.logger = logger
        self.util = Util()
        self.translations = self.util.loadTranslations(language)

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
    
    def aggregate(self, filteredRows):
        
        splitData = self.splitByIdentifier(filteredRows)

        aggregatedData = self.aggregateByIdentifier(splitData)

        return aggregatedData
