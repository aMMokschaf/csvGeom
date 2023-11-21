from csvGeom.enums.geoJsonType import GeoJsonType


class MultiLineString:

    def __init__(self):
        self.lineStrings = []
        self.type = GeoJsonType.MULTI_LINESTRING

    def add_line_string(self, line_string):
        self.lineStrings.append(line_string)

    def __str__(self):
        line_strings = ','.join(str(line_string.return_coordinates()) for line_string in self.lineStrings)

        return f'"type": "{GeoJsonType.MULTI_LINESTRING.get_geo_json_case()}", "coordinates" : [{line_strings}]'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': GeoJsonType.MULTI_LINESTRING.value,
            'coordinates': self.lineStrings
        }
