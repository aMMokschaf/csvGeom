from csvGeom.geojson.geojsonObject import GeoJsonObject

from csvGeom.enums.outputType import OutputType


class LineString(GeoJsonObject):

    def __init__(self):
        super().__init__()
        self.coordinates = []
        self.type = OutputType.LINESTRING

    def add_coordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def add_multiple_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def returnCoordinates(self):
        return self.coordinates

    def __str__(self):
        return f'"type": "{OutputType.LINESTRING.get_geo_json_case()}", "coordinates": {self.coordinates}'

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': OutputType.LINESTRING.value,
            'coordinates': self.coordinates
        }
