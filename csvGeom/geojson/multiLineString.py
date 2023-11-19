from csvGeom.enums.outputType import OutputType


class MultiLineString:

    def __init__(self):
        self.lineStrings = []
        self.type = OutputType.MULTI_LINESTRING

    def add_line_string(self, lineString):
        self.lineStrings.append(lineString)

    def __str__(self):
        line_strings = ','.join(str(l.returnCoordinates()) for l in self.lineStrings)

        return f'"type": "{OutputType.MULTI_LINESTRING.get_geo_json_case()}", "coordinates" : [{line_strings}]'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': OutputType.MULTI_LINESTRING.value,
            'coordinates': self.lineStrings
        }
