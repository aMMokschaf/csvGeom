from geojsonObject import GeoJsonObject

class Line(GeoJsonObject):

    def __init__(self):
        self.coordinates = []

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
    
    def addMultipleCoordinates(self, coordinates):
        self.coordinates.append(coordinates)
       