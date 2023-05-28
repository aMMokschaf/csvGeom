from geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class Line(GeoJsonObject):

    def __init__(self):
        self.coordinates = []

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
    
    def addMultipleCoordinates(self, coordinates):
        self.coordinates.append(coordinates)

    def __str__(self):
        return f"'type' : {OutputType.LINE.getTitleCase()} 'coordinates' : {self.coordinates}"

    def __dict__(self):
        return {
            'type' : OutputType.LINE.value,
            'coordinates': self.coordinates
        }
       