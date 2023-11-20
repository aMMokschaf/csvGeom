from csvGeom.utils.argParser import ArgParser
from csvGeom.csvGeomGui import CsvGeomGui
from csvGeom.csvGeomCli import CsvGeomCli
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.utils.logger import Logger


class Main:

    def __init__(self):
        self.argParser = ArgParser()
        self.args = self.argParser.args

    def main(self):
        if self.args.cli:
            cli = CsvGeomCli(self.args)
            cli.handle_cli()
        else:
            gui = CsvGeomGui(self.args)
            gui.handle_gui()


if __name__ == '__main__':
    app = Main()
    app.main()
