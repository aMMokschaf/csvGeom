from geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class Point(GeoJsonObject):

    def __init__(self, coordinates):
        self.coordinates = coordinates

    def __str__(self):
        return f"'type' : {OutputType.POINT.getTitleCase()} 'coordinates' : {self.coordinates}"
    
    def __dict__(self):
        return {
            'type' : OutputType.POINT.value,
            'coordinates': self.coordinates
        }