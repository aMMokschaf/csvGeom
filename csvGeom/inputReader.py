import csv
import io

from csvGeom.csvRow import CsvRow
from csvGeom.utils.util import Util
from csvGeom.utils.logger import Logger

DELIMITER = ','


class InputReader:

    def __init__(self, language):
        self.translations = Util.load_translations(language)

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
        except KeyError:
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
                    Logger.error(self.translations["err_missingColumn"])
                    break
                
            return rows
        
    def create_code_drop_down_entries(self, rows):
        codes = []

        for element in rows:
            if element.code not in codes:
                codes.append(element.code)

        Logger.info(self.translations["cli_uniqueCodes"], [len(codes), codes])

        return codes
        
    def filter_by_code(self, rows, code):
        elements = []

        for element in rows:
            if element.code == code:
                elements.append(element)

        Logger.info(self.translations["cli_filteredByCode"], [code])

        return elements
