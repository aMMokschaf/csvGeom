from geojson.geojsonObject import GeoJsonObject

from enums.outputType import OutputType

class Polygon(GeoJsonObject):

    def __init__(self):
        self.coordinates = []
        self.type = OutputType.POLYGON
    
    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
    
    def addMultipleCoordinate(self, coordinates):
        self.coordinates.append(coordinates)

    def __str__(self):
        return f"'type' : {OutputType.POLYGON.getGeoJSONCase()} 'coordinates' : {self.coordinates}"

    def __repr__(self):
        return str(self)
        
    def __dict__(self):
        return {
            'type' : OutputType.POLYGON.value,
            'coordinates': self.coordinates
        }