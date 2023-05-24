import io

from outputType import OutputType
from fileType import FileType

class FileWriter():

    def __init__(self):
        pass

    def writePolygonToFile(self, filename, data, fileType):
        suffix = OutputType.POLYGON.getAsSuffix() + fileType
        self.writeToFile(filename, data, suffix)

    def writeLineToFile(self):
        pass

    def writePointToFile(self):
        pass

    def writeToFile(self, filename, data, suffix):
        file = io.open(filename + suffix, "w")
        file.write(data)
        file.close()
