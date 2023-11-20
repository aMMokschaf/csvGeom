from csvGeom.utils.argParser import ArgParser
from csvGeom.csvGeomGui import CsvGeomGui
from csvGeom.csvGeomCli import CsvGeomCli


class Main:

    def __init__(self):
        self.argParser = ArgParser()
        self.args = self.argParser.args

    def main(self):
        if self.args.cli:
            csv_geom = CsvGeomCli(self.args)
            csv_geom.handle_cli()
        else:
            csv_geom = CsvGeomGui(self.args)
            csv_geom.handle_gui()


if __name__ == '__main__':
    app = Main()
    app.main()
