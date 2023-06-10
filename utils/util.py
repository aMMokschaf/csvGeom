import json

class Util():

    def getFileNameWithoutEnding(self, filename):
        return filename.rsplit(".", 1)[0]
    
    def createOutputFileName(self, fileName, geometryType, ending):
        outputFileName = self.getFileNameWithoutEnding(fileName)
        type = geometryType.getAsSuffix()
        fileEnding = ending.value
        
        return f"{outputFileName}{type}{fileEnding}"
    
    def loadTranslations(self, language):
        try:
            with open(f"./localization/{language}.json", "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations
        except:
            pass
    