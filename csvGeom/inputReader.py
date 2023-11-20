import csv
import io

from csvGeom.csvRow import CsvRow
from csvGeom.utils.util import Util

DELIMITER = ','


class InputReader:

    def __init__(self, language, logger):
        self.logger = logger
        self.util = Util()
        self.translations = self.util.load_translations(language)

    def parse_row(self, row):
        row_obj = CsvRow()
        try:
            row_obj.id = row['PtID']
            row_obj.east = row['East']
            row_obj.north = row['North']
            
            row_obj.code = row['Code']
            row_obj.identifier = row['Identifier']
        except:
            raise KeyError
        
        try:
            row_obj.height = row['Height']
        except:
            row_obj.height = "0"

        return row_obj

    def create_csv_row_list(self, inp_file_name):
        with io.open(inp_file_name) as impFile:
            rows = []

            reader = csv.DictReader(impFile, delimiter=DELIMITER)
            
            for row in reader:
                try:
                    row_obj = self.parse_row(row)
                    rows.append(row_obj)
                except KeyError:
                    self.logger.error(self.translations["err_missingColumn"])
                    break
                
            return rows
        
    def create_code_drop_down_entries(self, rows):
        codes = []

        for obj in rows:
            if obj.code not in codes:
                codes.append(obj.code)

        self.logger.info(self.translations["cli_uniqueCodes"], [len(codes), codes])

        return codes
        
    def filter_by_code(self, rows, code):
        list = []

        for obj in rows:
            if obj.code == code:
                list.append(obj)

        self.logger.info(self.translations["cli_filteredByCode"], [code])

        return list
