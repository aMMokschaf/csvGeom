class Util():

    def getFileNameWithoutEnding(self, filename):
        return filename.rsplit(".", 1)[0]
    
    def createOutputFileName(self, fileName, geometryType, ending):
        outputFileName = self.getFileNameWithoutEnding(fileName)
        type = geometryType.getAsSuffix()
        fileEnding = ending.value
        
        return f"{outputFileName}{type}{fileEnding}"
    