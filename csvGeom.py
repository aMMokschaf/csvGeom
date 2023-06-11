from csvGeom.utils.argParser import ArgParser
from csvGeom.csvGeomGui import CsvGeomGui
from csvGeom.csvGeomCli import CsvGeomCli

class Main():

    def __init__(self):
        self.argParser = ArgParser()

        self.args = self.argParser.args
        
    def main(self):
        if self.args.cli:
            cli = CsvGeomCli(self.args)
            cli.handleCli()
        else:
            gui = CsvGeomGui(self.args)
            gui.handleGui()

if __name__ == '__main__':
    app = Main()
    app.main()
