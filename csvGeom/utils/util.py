import json
from localization.default import default_localization


class Util:

    @staticmethod
    def get_file_name_without_ending(filename):
        return filename.rsplit(".", 1)[0]

    @staticmethod
    def create_output_file_name(file_name, geometry_type, ending):
        output_file_name = Util.get_file_name_without_ending(file_name)
        geometry_type = geometry_type.get_as_suffix()
        file_ending = ending.value

        return f"{output_file_name}{geometry_type}{file_ending}"

    @staticmethod
    def load_translations(language):
        try:
            with open(f"./localization/{language}.json", "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations
        except:
            return default_localization

    @staticmethod
    def create_formatted_msg(msg, replacements):
        formatted_msg = msg

        replacement_strings = [str(element) for element in replacements]

        for index, replacement in enumerate(replacement_strings):
            to_be_replaced = f"{{{index}}}"
            formatted_msg = formatted_msg.replace(to_be_replaced, replacement)

        return formatted_msg

    @staticmethod
    def get_first_element(elements):
        if len(elements) == 0:
            raise IndexError
        else:
            return elements[0]

    @staticmethod
    def get_identifier_from_list(elements):
        try:
            first_element = Util.get_first_element(elements)
            return first_element.identifier
        except IndexError:
            raise IndexError
