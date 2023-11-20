from csvGeom.utils.util import Util


class Aggregator:

    def __init__(self, language, logger):
        self.logger = logger
        self.util = Util()
        self.translations = self.util.load_translations(language)

    def get_all_unique_identifiers(self, lists):
        identifiers = []

        for element in lists:
            identifier = self.util.get_identifier_from_list(element)

            if identifier not in identifiers:
                identifiers.append(identifier)

        self.logger.info(self.translations["cli_uniqueIdentifiers"], [len(identifiers), identifiers])

        return identifiers    

    def aggregate_by_identifier(self, split_list):
        identifiers = self.get_all_unique_identifiers(split_list)

        geometry_wrapper = []
        geometry_list = []

        for identifier in identifiers:
            for item in split_list:
                if identifier == self.util.get_identifier_from_list(item):
                    geometry_wrapper.append(item)
            geometry_list.append(geometry_wrapper)
            geometry_wrapper = []

        self.logger.info(self.translations["cli_aggregatedGeometries"], [len(geometry_list)])

        return geometry_list
    
    def split_by_identifier(self, rows):
        if len(rows) == 0:
            return []
        
        lists = []
        element = []
        lists.append(element)
        
        identifier = self.util.get_identifier_from_list(rows)

        for row in rows:
            if row.identifier == identifier:
                element.append(row)
            else:
                identifier = row.identifier
                element = [row]
                lists.append(element)

        return lists
    
    def aggregate(self, filtered_rows):
        
        split_data = self.split_by_identifier(filtered_rows)

        aggregated_data = self.aggregate_by_identifier(split_data)

        return aggregated_data
