
TAB = "    " # Four Spaces

class Util():
    def indent(self, n):
        indent = TAB * n
        indent = "\n" + indent
        return indent
    
    def getFileNameWithoutSuffix(self, filename):
        return filename.rsplit(".", 1)[0]
    
    def createOutputFileName(self, fileName, suffix, ending):
        outputFileName = self.getFileNameWithoutSuffix(fileName)
        typeSuffix = suffix.getAsSuffix()
        fileEnding = ending.value
        
        return f"{outputFileName}{typeSuffix}{fileEnding}"
    
