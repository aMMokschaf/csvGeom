from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class LineString(GeoJsonObject):

    def __init__(self):
        self.coordinates = []
        self.type = OutputType.LINESTRING

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
    
    def addMultipleCoordinates(self, coordinates):
        self.coordinates.append(coordinates)
    
    def returnCoordinates(self, coordinates):
        return self.coordinates

    def __str__(self):
        return f"'type': '{OutputType.LINESTRING.getGeoJSONCase()}', 'coordinates': {self.coordinates}"

    def __repr__(self):
        return str(self)

    def __dict__(self):
        return {
            'type': OutputType.LINESTRING.value,
            'coordinates': self.coordinates
        }
       