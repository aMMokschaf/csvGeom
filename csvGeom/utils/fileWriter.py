import io

from csvGeom.utils.logger import Logger

class FileWriter():

    def __init__(self):
        self.logger = Logger()

    def writeToFile(self, data, filename):
        try:
            file = io.open(filename, "w")
            file.write(data)
            file.close()

            self.logger.info(f"File succesfully written: {filename}")
            
        except FileNotFoundError:
            self.logger.error("File not found!")
        except PermissionError:
            self.logger.error("You don't have permission to write this file.")
        except IOError:
            self.logger.error(f"Error while writing the file {filename}.")
