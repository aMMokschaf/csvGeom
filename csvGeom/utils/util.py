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
    
    def createFormattedMsg(self, msg, replacements):
        formattedMsg = msg

        replacementStrings = [str(element) for element in replacements]

        for index, replacement in enumerate(replacementStrings):
            toBeReplaced = f"{{{index}}}"
            formattedMsg = formattedMsg.replace(toBeReplaced, replacement)

        return formattedMsg

    def getFirstElement(self, list):
        if len(list) == 0:
            raise IndexError
        else:
            return list[0]

    def getIdentifierFromList(self, list):
        try:
            firstElement = self.getFirstElement(list)
            return firstElement.identifier
        except IndexError:
            raise IndexError
