import csv
import io

DELIMITER = ','

class InputReader():

    def __init__(self):
        pass

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
                list.append(obj)

        return list
