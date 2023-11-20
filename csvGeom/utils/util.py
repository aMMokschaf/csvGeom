import json
from localization.default import default_localization


class Util:

    def get_file_name_without_ending(self, filename):
        return filename.rsplit(".", 1)[0]
    
    def create_output_file_name(self, file_name, geometry_type, ending):
        outputFileName = self.get_file_name_without_ending(file_name)
        type = geometry_type.get_as_suffix()
        file_ending = ending.value
        
        return f"{outputFileName}{type}{file_ending}"
    
    def load_translations(self, language):
        try:
            with open(f"./localization/{language}.json", "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations
        except:
            return default_localization
    
    def create_formatted_msg(self, msg, replacements):
        formatted_msg = msg

        replacement_strings = [str(element) for element in replacements]

        for index, replacement in enumerate(replacement_strings):
            to_be_replaced = f"{{{index}}}"
            formatted_msg = formatted_msg.replace(to_be_replaced, replacement)

        return formatted_msg

    def get_first_element(self, list):
        if len(list) == 0:
            raise IndexError
        else:
            return list[0]

    def get_identifier_from_list(self, list):
        try:
            first_element = self.get_first_element(list)
            return first_element.identifier
        except IndexError:
            raise IndexError
