from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class Point(GeoJsonObject):

    def __init__(self):
        self.coordinates = []
        self.type = OutputType.POINT

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def __str__(self):
        return f"'type' : {OutputType.POINT.getGeoJSONCase()} 'coordinates' : {self.coordinates}"
    
    def __dict__(self):
        return {
            'type' : OutputType.POINT.value,
            'coordinates': self.coordinates
        }