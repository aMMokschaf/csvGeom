import PySimpleGUI as sG

from csvGeom.gui import Gui
from csvGeom.inputReader import InputReader
from csvGeom.modeller import Modeller
from csvGeom.utils.util import Util
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.enums.outputType import OutputType
from csvGeom.enums.fileType import FileType
from csvGeom.validator import Validator
from csvGeom.aggregator import Aggregator


class CsvGeomGui:

    def __init__(self, args):
        self.args = args

        self.modeller = Modeller(args.l)
        self.inputReader = InputReader(args.l)
        self.aggregator = Aggregator(args.l)

        self.rows = None
        self.filteredRows = None

        self.selectedFileName = None
        self.selectedType = OutputType.POLYGON
        self.selectedFileType = FileType.GEO_JSON

        self.gui = Gui("csvGeom v0.6.0", self.args.l)

    def reset_errors(self):
        self.modeller.errCount = 0
        self.gui.reset_err_msg()

    def handle_input(self, values):
        self.reset_errors()

        self.selectedFileName = values['-INPUT-']
        self.rows = self.inputReader.create_csv_row_list(self.selectedFileName)

        entries = self.inputReader.create_code_drop_down_entries(self.rows)
        self.gui.update_values("-CODE-", entries)
        self.gui.enable_element("-CODE-")
        
        self.gui.disable_element("-CONVERT-")

    def handle_code(self, values):
        self.reset_errors()

        selected_code = values['-CODE-']
        self.filteredRows = self.inputReader.filter_by_code(self.rows, selected_code)

        self.gui.enable_element("-CONVERT-")

    def handle_convert(self):
        self.reset_errors()

        aggregated_data = self.aggregator.aggregate(self.filteredRows)

        feature_collection_model = self.modeller.create_feature_collection(aggregated_data, self.selectedType)

        validator = Validator(self.args.l)

        validated_model = validator.validate(feature_collection_model)

        err_count = validator.errCount
        self.gui.update_err_msg(err_count)
        
        output = str(validated_model)

        output_file_name = Util.create_output_file_name(self.selectedFileName, self.selectedType, self.selectedFileType)
        
        FileWriter.write_to_file(output, output_file_name)

    def handle_gui(self):
        while True:
            event, values = self.gui.read_values()

            if event == "-INPUT-":
                self.handle_input(values)

            if event == "-CODE-":
                self.handle_code(values)

            if event == "-GEOM_POINT-":
                self.selectedType = OutputType.POINT

            if event == "-GEOM_LINESTRING-":
                self.selectedType = OutputType.LINESTRING

            if event == "-GEOM_POLYGON-":
                self.selectedType = OutputType.POLYGON

            if event == "-CONVERT-":
                self.handle_convert()

            if event == "-CLOSE-" or event == sG.WIN_CLOSED:
                break

        self.gui.destroy()       
