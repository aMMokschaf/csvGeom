from geojson.geojsonObject import GeoJsonObject

class Polygon(GeoJsonObject):

    def __init__(self):
        self.coordinates = []
    
    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
    
    def addMultipleCoordinate(self, coordinates):
        self.coordinates.append(coordinates)
