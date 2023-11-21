from csvGeom.enums.geoJsonType import GeoJsonType


class LineString:

    def __init__(self):
        self.coordinates = []
        self.type = GeoJsonType.LINESTRING

    def add_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def add_multiple_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def return_coordinates(self):
        return self.coordinates

    def __str__(self):
        return f'"type": "{GeoJsonType.LINESTRING.get_geo_json_case()}", "coordinates": {self.coordinates}'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': GeoJsonType.LINESTRING.value,
            'coordinates': self.coordinates
        }
