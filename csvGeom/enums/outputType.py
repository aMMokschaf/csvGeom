from enum import Enum


class OutputType(Enum):
    POINT = "Point"
    LINESTRING = "LineString"
    POLYGON = "Polygon"
    MULTI_POINT = "MultiPoint"
    MULTI_LINESTRING = "MultiLineString"
    MULTI_POLYGON = "MultiPolygon"

    def get_geo_json_case(self):
        return self.value

    def get_upper_case(self):
        return self.value.upper()

    def get_lower_case(self):
        return self.value.lower()

    def get_title_case(self):
        return self.value.title()

    def get_as_suffix(self):
        return "_" + self.get_lower_case()
