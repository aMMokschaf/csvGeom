from utils.argParser import ArgParser
from csvGeomGui import CsvGeomGui
from csvGeomCli import CsvGeomCli

class Main():

    def __init__(self):
        self.argParser = ArgParser()

        self.args = self.argParser.args
        
    def main(self):
        if self.args.cli:
            CsvGeomCli(self.args)
        else:
            gui = CsvGeomGui(self.args)
            gui.handleGui()

if __name__ == '__main__':
    app = Main()
    app.main()
