import io

from csvGeom.utils.util import Util

class FileWriter():

    def __init__(self):
        self.util = Util()

    def write(self, data, filename, mode):
        try:
            file = io.open(filename, mode)
            file.write(data)
            file.close()
        except:
            raise Exception

    def writeToFile(self, data, filename):
        try:
            self.write(data, filename, "w")
        except:
            raise Exception

    def appendToFile(self, data, filename):
        try:
            self.write(data, filename, "a")
        except:
            raise Exception
        