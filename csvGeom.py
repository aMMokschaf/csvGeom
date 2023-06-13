from csvGeom.utils.argParser import ArgParser
from csvGeom.csvGeomGui import CsvGeomGui
from csvGeom.csvGeomCli import CsvGeomCli
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.utils.logger import Logger

class Main():

    def __init__(self):
        self.argParser = ArgParser()
        self.args = self.argParser.args

        self.writer = FileWriter()
        self.logger = Logger(self.writer)
        
    def main(self):
        if self.args.cli:
            cli = CsvGeomCli(self.args, self.logger)
            cli.handleCli()
        else:
            gui = CsvGeomGui(self.args, self.logger)
            gui.handleGui()

if __name__ == '__main__':
    app = Main()
    app.main()
