from csvGeom.geojson.geojsonObject import GeoJsonObject

from csvGeom.enums.outputType import OutputType


class Polygon(GeoJsonObject):

    def __init__(self):
        super().__init__()
        self.coordinates = []
        self.type = OutputType.POLYGON

    def add_coordinate(self, coordinate):
        self.coordinates.append(coordinate)
   
    def add_multiple_coordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def returnCoordinates(self):
        return self.coordinates

    def __str__(self): 
        return f'"type": "{OutputType.POLYGON.get_geo_json_case()}","coordinates": [{self.coordinates}]'

    def __repr__(self):
        return str(self)
        
    def __dict__(self):
        return {
            'type': OutputType.POLYGON.value,
            'coordinates': self.coordinates
        }