import io

from csvGeom.utils.logger import Logger
from csvGeom.utils.util import Util

class FileWriter():

    def __init__(self, language):
        self.logger = Logger()
        self.util = Util()
        self.translations = self.util.loadTranslations(language)

    def writeToFile(self, data, filename):
        try:
            file = io.open(filename, "w")
            file.write(data)
            file.close()

            self.logger.info(self.translations["cli_fileWritten"], [filename])
            
        except FileNotFoundError:
            self.logger.error(self.translations["err_fileNotFound"])
        except PermissionError:
            self.logger.error(self.translations["err_permissionError"])
        except IOError:
            self.logger.error(self.translations["err_io"], [filename])
