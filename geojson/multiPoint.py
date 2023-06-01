from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class MultiPoint(GeoJsonObject):

    def __init__(self):
        self.coordinates = []
        self.type = OutputType.MULTI_POINT

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def __str__(self):
        return f"'type' : {OutputType.MULTI_POINT.getTitleCase()} 'coordinates' : {self.coordinates}"
    
    def __dict__(self):
        return {
            'type' : OutputType.MULTI_POINT.value,
            'coordinates': self.coordinates
        }