from geojsonObject import GeoJsonObject

from outputType import OutputType

class Point(GeoJsonObject):

    def __init__(self, coordinate):
        self.coordinate = coordinate

    def __str__(self):
        return f"'type' : {OutputType.POINT.getTitleCase()} 'coordinates' : {self.coordinate}"
    
    def __dict__(self):
        return {
            'type' : OutputType.POINT.value,
            'coordinates': self.coordinate
        }