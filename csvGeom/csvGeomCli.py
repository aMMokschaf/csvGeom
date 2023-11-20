from csvGeom.inputReader import InputReader
from csvGeom.modeller import Modeller
from csvGeom.aggregator import Aggregator
from csvGeom.utils.util import Util
from csvGeom.utils.logger import Logger
from csvGeom.utils.fileWriter import FileWriter
from csvGeom.enums.outputType import OutputType
from csvGeom.enums.fileType import FileType
from csvGeom.validator import Validator


class CsvGeomCli:

    def __init__(self, args):
        self.args = args

        self.translations = Util.load_translations(args.l)
        self.inputReader = InputReader(args.l)
        self.aggregator = Aggregator(args.l)

        self.selectedFileType = FileType.GEO_JSON

    def parse_geometry_type(self, arg):
        try:
            geometry_type = OutputType(arg)
        except ValueError:
            Logger.error(self.translations["err_parseGeometry"], [arg])
            geometry_type = OutputType.POLYGON

        return geometry_type

    def check_valid_code_selection(self, entries, selection):
        if selection in entries:
            return True
        else:
            return False
        
    def handle_code_selection(self, entries):
        while True:
            msg = Util.create_formatted_msg(self.translations["cli_selectCode"], [len(entries), entries])

            selected_code = input(msg)
            if self.check_valid_code_selection(entries, selected_code):
                Logger.info(self.translations["cli_codeSelected"], [selected_code])
                return selected_code
            else:
                Logger.error(self.translations["err_invalidCode"], [selected_code])

    def handle_output_path(self, selected_file_name, selected_type):
        output_file_path = self.args.o

        if self.args.o == "" or self.args.o is None:
            output_file_path = Util.create_output_file_name(selected_file_name, selected_type, self.selectedFileType)

        return output_file_path
                
    def handle_cli(self):
        selected_file_name = self.args.i

        selected_type = self.parse_geometry_type(self.args.g)

        rows = self.inputReader.create_csv_row_list(selected_file_name)

        entries = self.inputReader.create_code_drop_down_entries(rows)

        selected_code = self.handle_code_selection(entries)

        filtered_rows = self.inputReader.filter_by_code(rows, selected_code)

        split_data = self.aggregator.split_by_identifier(filtered_rows)

        aggregated_data = self.aggregator.aggregate_by_identifier(split_data)

        feature_collection_model = Modeller.create_feature_collection(aggregated_data, selected_type)

        validator = Validator(self.args.l)

        valid_model = validator.validate(feature_collection_model)

        output = str(valid_model)

        output_file_path = self.handle_output_path(selected_file_name, selected_type)

        print("outputfilePath", output_file_path)

        try:
            FileWriter.write_to_file(output, output_file_path)
        except:
            Logger.error(self.translations["err_io"], [output_file_path])
